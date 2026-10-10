import re
import uuid
from urllib.parse import quote

from django.db import models
from django.utils.text import slugify

LEVEL_CHOICES = [
    ("diploma", "Diploma / Certificate"),
    ("undergraduate", "Bachelor's (Undergraduate)"),
    ("postgraduate", "Master's (Postgraduate)"),
    ("phd", "PhD / Research"),
    ("other", "Not sure yet"),
]


class SiteSettings(models.Model):
    """Single row holding site-wide text, contact details and home-page headings."""
    site_name = models.CharField(max_length=120, default="Bhumi Pathways Consultancy")
    tagline = models.CharField(max_length=200, default="Study abroad & education counselling")
    announcement_text = models.CharField(
        max_length=250, blank=True, default="Counselling by appointment. Talk to us on WhatsApp or request a call back.",
        help_text="Thin bar at the very top of every page. Leave empty to hide it.")
    cta_label = models.CharField("Main button label", max_length=40, default="Book a consultation")
    phone = models.CharField(max_length=40, default="+91 00000 00000")
    email = models.EmailField(default="info@bhumipathwaysconsultancy.com")
    whatsapp_number = models.CharField(
        max_length=20, default="910000000000", help_text="Digits only with country code, e.g. 919876543210.")
    whatsapp_message = models.CharField(
        max_length=200, default="Hello Bhumi Pathways, I would like to talk to a counsellor.")
    address = models.TextField(default="Office address to be added")
    office_hours = models.CharField(max_length=200, blank=True, default="")
    footer_about = models.TextField(
        default="Study abroad counselling, application support and visa documentation guidance. We advise honestly and never promise admissions or visa outcomes.")
    default_meta_description = models.TextField(
        default="Bhumi Pathways Consultancy offers study abroad counselling, university application support and visa documentation guidance for students.")
    notification_emails = models.CharField(
        max_length=300, blank=True, help_text="Comma-separated emails that receive new-enquiry alerts (used when ENQUIRY_NOTIFY_EMAILS is not set in .env).")
    # Home page section headings
    home_destinations_title = models.CharField(max_length=150, default="Where would you like to study?")
    home_destinations_intro = models.TextField(
        blank=True, default="Six destinations we currently advise on. Details such as intakes and requirements change, so we confirm them for your chosen course.")
    home_services_title = models.CharField(max_length=150, default="How we help")
    home_services_intro = models.TextField(blank=True, default="Support at each stage, with you making the final decisions.")
    home_steps_title = models.CharField(max_length=150, default="Your pathway, step by step")
    home_cta_title = models.CharField(max_length=150, default="Talk to a counsellor before you decide.")
    home_cta_text = models.TextField(
        default="Tell us where you are in your journey. We will respond using the contact details you provide. We do not guarantee admissions or visa outcomes; we help you prepare the strongest honest application.")
    seeded = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def phone_href(self):
        return re.sub(r"[^\d+]", "", self.phone)

    def whatsapp_url(self):
        digits = re.sub(r"\D", "", self.whatsapp_number)
        return f"https://wa.me/{digits}?text={quote(self.whatsapp_message)}"

    def __str__(self):
        return "Site settings"


class PageContent(models.Model):
    class Slug(models.TextChoices):
        HOME = "home", "Home"
        ABOUT = "about", "About Us"
        SERVICES = "services", "Services"
        DESTINATIONS = "destinations", "Study Destinations"
        VISA = "visa", "Visa Assistance"
        FAQS = "faqs", "FAQs"
        CONTACT = "contact", "Contact"
        PRIVACY = "privacy", "Privacy Policy"
        TERMS = "terms", "Terms of Use"

    slug = models.CharField(max_length=20, unique=True, choices=Slug.choices)
    seo_title = models.CharField("Browser / Google title", max_length=70, blank=True,
                                 help_text="Shown in the browser tab and search results. Site name is added automatically.")
    meta_description = models.TextField("Google description", max_length=320, blank=True)
    eyebrow = models.CharField("Small line above heading", max_length=100, blank=True)
    hero_title = models.CharField("Main heading", max_length=200, blank=True)
    hero_text = models.TextField("Text under heading", blank=True)
    section_title = models.CharField("Section heading", max_length=150, blank=True,
                                     help_text="Heading for the page's list section (principles, steps or documents).")
    section_intro = models.TextField("Section intro", blank=True)
    body = models.TextField("Main content (HTML allowed)", blank=True,
                            help_text="You can use simple HTML such as <h2>, <p>, <ul><li>, <strong>, <a href>. Only trusted staff can edit this.")
    notice = models.TextField("Notice box", blank=True, help_text="Highlighted note on the page. Leave empty to hide it.")

    class Meta:
        verbose_name = "Page content"
        verbose_name_plural = "Page content"
        ordering = ["id"]

    @classmethod
    def for_slug(cls, slug):
        from .defaults import PAGES
        obj, _ = cls.objects.get_or_create(slug=slug, defaults=PAGES.get(slug, {}))
        return obj

    def __str__(self):
        return self.get_slug_display()


class Orderable(models.Model):
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    is_active = models.BooleanField("Show on website", default=True)

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class MenuItem(Orderable):
    class Location(models.TextChoices):
        HEADER = "header", "Top menu"
        FOOTER = "footer", "Footer: Explore column"
        LEGAL = "legal", "Footer: bottom links"

    location = models.CharField(max_length=10, choices=Location.choices, default=Location.HEADER)
    label = models.CharField(max_length=60)
    url = models.CharField(max_length=300, help_text="Page path like /about/ or a full link like https://example.com")
    new_tab = models.BooleanField("Open in new tab", default=False)

    class Meta(Orderable.Meta):
        verbose_name = "Menu link"
        verbose_name_plural = "Menu links"
        ordering = ["location", "order", "id"]

    def __str__(self):
        return f"{self.get_location_display()}: {self.label}"


class Destination(Orderable):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=90, unique=True, blank=True, help_text="Auto-filled from the name.")
    flag = models.CharField("Flag emoji", max_length=10, blank=True)
    intro = models.TextField()
    intakes = models.CharField("Typical intakes", max_length=200, blank=True)
    points = models.TextField("Key points", blank=True, help_text="One point per line.")

    class Meta(Orderable.Meta):
        verbose_name = "Study destination"
        verbose_name_plural = "Study destinations"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "destination"
            slug, n = base, 2
            while Destination.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug, n = f"{base}-{n}", n + 1
            self.slug = slug
        super().save(*args, **kwargs)

    def point_list(self):
        return [p.strip() for p in self.points.splitlines() if p.strip()]

    def __str__(self):
        return self.name


class Service(Orderable):
    title = models.CharField(max_length=120)
    text = models.TextField()

    class Meta(Orderable.Meta):
        verbose_name = "Service"

    def __str__(self):
        return self.title


class ProcessStep(Orderable):
    title = models.CharField(max_length=120)
    text = models.CharField(max_length=250, blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "Process step"

    def __str__(self):
        return self.title


class Principle(Orderable):
    title = models.CharField(max_length=120)
    text = models.TextField()

    class Meta(Orderable.Meta):
        verbose_name = "About page principle"

    def __str__(self):
        return self.title


class VisaDocument(Orderable):
    text = models.CharField("Document", max_length=200)

    class Meta(Orderable.Meta):
        verbose_name = "Visa document"

    def __str__(self):
        return self.text


class FAQ(Orderable):
    question = models.CharField(max_length=250)
    answer = models.TextField()

    class Meta(Orderable.Meta):
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class Enquiry(models.Model):
    class Type(models.TextChoices):
        CONSULTATION = "consultation", "Consultation"
        VISA = "visa", "Visa assistance"
        GENERAL = "general", "General enquiry"

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        IN_PROGRESS = "in_progress", "In progress"
        CLOSED = "closed", "Closed"

    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    enquiry_type = models.CharField(max_length=20, choices=Type.choices, default=Type.CONSULTATION)
    country_interest = models.CharField(max_length=60, blank=True)
    study_level = models.CharField(max_length=40, choices=LEVEL_CHOICES, blank=True)
    message = models.TextField(max_length=2000, blank=True)
    consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"
        indexes = [models.Index(fields=["status", "-created_at"], name="enq_status_created_idx")]

    def __str__(self):
        return f"{self.name} ({self.get_enquiry_type_display()})"
