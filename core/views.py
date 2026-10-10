import json

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .emails import send_enquiry_notifications
from .forms import EnquiryForm
from .models import (FAQ, LEVEL_CHOICES, Destination, Enquiry, PageContent, Principle, ProcessStep,
                     Service, SiteSettings, VisaDocument)


def _ld(data):
    """JSON-LD safe to embed in a <script> tag."""
    return json.dumps(data).replace("<", "\\u003c")


def _render(request, template, slug, status=200, **ctx):
    ctx["page"] = PageContent.for_slug(slug)
    return render(request, template, ctx, status=status)


def _client_ip(request):
    if settings.BEHIND_PROXY:
        xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if xff:
            return xff.split(",")[-1].strip()  # last hop = address Nginx saw
    return request.META.get("REMOTE_ADDR", "unknown")


def _rate_key(request):
    return f"enquiry-rate:{_client_ip(request)}"


def _over_limit(request):
    return cache.get(_rate_key(request), 0) >= settings.ENQUIRY_RATE_LIMIT


def _record_submission(request):
    key = _rate_key(request)
    cache.add(key, 0, 3600)
    try:
        cache.incr(key)
    except ValueError:
        cache.set(key, 1, 3600)


def home(request):
    site = SiteSettings.load()
    ld = {"@context": "https://schema.org", "@type": "EducationalOrganization", "name": site.site_name,
          "url": request.build_absolute_uri("/"), "email": site.email}
    return _render(request, "core/home.html", "home",
                   destinations=Destination.objects.filter(is_active=True),
                   services=Service.objects.filter(is_active=True),
                   steps=ProcessStep.objects.filter(is_active=True),
                   levels=LEVEL_CHOICES, form=EnquiryForm(initial={"enquiry_type": "consultation"}),
                   json_ld=_ld(ld))


def about(request):
    return _render(request, "core/about.html", "about", principles=Principle.objects.filter(is_active=True))


def services(request):
    return _render(request, "core/services.html", "services",
                   services=Service.objects.filter(is_active=True),
                   steps=ProcessStep.objects.filter(is_active=True))


def destinations(request):
    return _render(request, "core/destinations.html", "destinations",
                   destinations=Destination.objects.filter(is_active=True))


def visa(request):
    return _render(request, "core/visa.html", "visa", documents=VisaDocument.objects.filter(is_active=True))


def faqs(request):
    items = FAQ.objects.filter(is_active=True)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": f.question,
                          "acceptedAnswer": {"@type": "Answer", "text": f.answer}} for f in items]}
    return _render(request, "core/faqs.html", "faqs", faqs=items, json_ld=_ld(ld))


def legal(request, slug):
    return _render(request, "core/legal.html", slug)


def _initial_from_query(request):
    initial = {"enquiry_type": "visa" if request.GET.get("type") == "visa" else "consultation"}
    country = request.GET.get("country", "")
    if Destination.objects.filter(is_active=True, name=country).exists():
        initial["country_interest"] = country
    level = request.GET.get("level", "")
    if level in dict(LEVEL_CHOICES):
        initial["study_level"] = level
    return initial


def contact(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get("website"):  # honeypot filled: pretend success, store nothing
                request.session["enquiry_ref"] = ""
                return redirect("thanks")
            if _over_limit(request):
                form.add_error(None, "Too many enquiries were sent from your network. Please try again later or message us on WhatsApp.")
                return _render(request, "core/contact.html", "contact", status=429, form=form)
            enquiry = form.save()
            _record_submission(request)
            send_enquiry_notifications(enquiry)
            request.session["enquiry_ref"] = str(enquiry.reference)
            return redirect("thanks")
        return _render(request, "core/contact.html", "contact", status=400, form=form)
    return _render(request, "core/contact.html", "contact", form=EnquiryForm(initial=_initial_from_query(request)))


def thanks(request):
    ref = request.session.pop("enquiry_ref", "")
    return _render(request, "core/thanks.html", "contact", reference=ref, noindex=True)


def robots_txt(request):
    lines = ["User-agent: *", "Allow: /", "Disallow: /admin/", "Disallow: /contact/thank-you/", "",
             f"Sitemap: {request.build_absolute_uri(reverse('sitemap'))}", ""]
    return HttpResponse("\n".join(lines), content_type="text/plain")
