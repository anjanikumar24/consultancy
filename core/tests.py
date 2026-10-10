from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Destination, Enquiry, PageContent, SiteSettings

PAYLOAD = {"name": "Asha Verma", "email": "Asha@Example.com", "phone": "+91 98765 43210",
           "enquiry_type": "consultation", "country_interest": "Canada", "study_level": "postgraduate",
           "message": "Need help choosing a course.", "consent": "on"}
PAGE_NAMES = ["home", "about", "services", "destinations", "visa", "faqs", "contact", "privacy", "terms"]


class PublicPageTests(TestCase):
    def test_all_pages_render(self):
        for name in PAGE_NAMES:
            with self.subTest(page=name):
                r = self.client.get(reverse(name))
                self.assertEqual(r.status_code, 200)
                self.assertContains(r, "<title>")

    def test_seeded_content_present(self):
        r = self.client.get(reverse("destinations"))
        self.assertContains(r, "United Kingdom")
        self.assertContains(self.client.get(reverse("faqs")), "guarantee admission")

    def test_sitemap_and_robots(self):
        self.assertContains(self.client.get("/sitemap.xml"), "/about/")
        self.assertContains(self.client.get("/robots.txt"), "Sitemap:")

    def test_unknown_page_404(self):
        self.assertEqual(self.client.get("/nope/").status_code, 404)


class EditableContentTests(TestCase):
    """Whatever staff change in the database must show on the website."""

    def test_site_settings_edit_appears(self):
        s = SiteSettings.load()
        s.phone, s.site_name = "+91 11111 22222", "Renamed Consultancy"
        s.save()
        r = self.client.get(reverse("home"))
        self.assertContains(r, "+91 11111 22222")
        self.assertContains(r, "Renamed Consultancy")

    def test_page_content_edit_appears(self):
        p = PageContent.for_slug("about")
        p.hero_title = "A brand new heading"
        p.save()
        self.assertContains(self.client.get(reverse("about")), "A brand new heading")

    def test_inactive_destination_hidden(self):
        Destination.objects.filter(name="Ireland").update(is_active=False)
        self.assertNotContains(self.client.get(reverse("destinations")), 'id="ireland"')

    def test_new_destination_appears(self):
        Destination.objects.create(name="New Zealand", flag="🇳🇿", intro="Test intro text.")
        self.assertContains(self.client.get(reverse("home")), "New Zealand")


@override_settings(ENQUIRY_NOTIFY_EMAILS=["staff@example.com"], ENQUIRY_SEND_ACKNOWLEDGEMENT=True)
class EnquiryTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_valid_post_saves_and_emails(self):
        r = self.client.post(reverse("contact"), PAYLOAD)
        self.assertRedirects(r, reverse("thanks"))
        e = Enquiry.objects.get()
        self.assertEqual((e.email, e.status), ("asha@example.com", "new"))
        self.assertEqual(len(mail.outbox), 2)

    def test_invalid_post_shows_errors_and_saves_nothing(self):
        r = self.client.post(reverse("contact"), {**PAYLOAD, "email": "nope", "phone": "abc"})
        self.assertEqual(r.status_code, 400)
        self.assertContains(r, "Enter a valid phone number", status_code=400)
        self.assertEqual(Enquiry.objects.count(), 0)

    def test_consent_required(self):
        data = {k: v for k, v in PAYLOAD.items() if k != "consent"}
        self.assertEqual(self.client.post(reverse("contact"), data).status_code, 400)
        self.assertEqual(Enquiry.objects.count(), 0)

    def test_honeypot_not_saved(self):
        r = self.client.post(reverse("contact"), {**PAYLOAD, "website": "http://spam"})
        self.assertRedirects(r, reverse("thanks"))
        self.assertEqual(Enquiry.objects.count(), 0)

    def test_header_injection_safe(self):
        self.client.post(reverse("contact"), {**PAYLOAD, "name": "Eve\r\nBcc: x@evil.com"})
        self.assertNotIn("\n", mail.outbox[0].subject)

    @override_settings(ENQUIRY_RATE_LIMIT=1)
    def test_rate_limit(self):
        self.client.post(reverse("contact"), PAYLOAD)
        r = self.client.post(reverse("contact"), PAYLOAD)
        self.assertEqual(r.status_code, 429)
        self.assertEqual(Enquiry.objects.count(), 1)

    def test_csrf_enforced(self):
        from django.test import Client
        r = Client(enforce_csrf_checks=True).post(reverse("contact"), PAYLOAD)
        self.assertEqual(r.status_code, 403)

    def test_prefill_from_query(self):
        r = self.client.get(reverse("contact"), {"country": "Germany", "level": "phd", "type": "visa"})
        self.assertContains(r, 'value="visa"')
        self.assertContains(r, '<option value="Germany" selected>')


class AdminTests(TestCase):
    def setUp(self):
        U = get_user_model()
        self.admin = U.objects.create_superuser("boss", "b@example.com", "Str0ng-pass-phrase!")
        self.enq = Enquiry.objects.create(name="A", email="a@example.com", phone="+911234567890", consent=True)

    def test_admin_requires_login(self):
        self.assertEqual(self.client.get("/admin/core/enquiry/").status_code, 302)

    def test_admin_pages_open(self):
        self.client.force_login(self.admin)
        for url in ["/admin/", "/admin/core/enquiry/", "/admin/core/pagecontent/", "/admin/core/destination/",
                    "/admin/core/faq/", "/admin/core/menuitem/", f"/admin/core/enquiry/{self.enq.pk}/change/"]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_site_settings_goes_straight_to_form(self):
        self.client.force_login(self.admin)
        r = self.client.get("/admin/core/sitesettings/")
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r.url.endswith("/admin/core/sitesettings/1/change/"))

    def test_status_action_and_csv(self):
        self.client.force_login(self.admin)
        r = self.client.post("/admin/core/enquiry/", {"action": "mark_contacted", "_selected_action": [self.enq.pk]})
        self.assertEqual(r.status_code, 302)
        self.enq.refresh_from_db()
        self.assertEqual(self.enq.status, "contacted")
        r = self.client.post("/admin/core/enquiry/", {"action": "export_csv", "_selected_action": [self.enq.pk]})
        self.assertEqual(r["Content-Type"], "text/csv")
