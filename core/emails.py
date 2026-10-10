import logging

from django.conf import settings
from django.core.mail import send_mail

from .models import SiteSettings

logger = logging.getLogger(__name__)


def _one_line(value):
    return " ".join(str(value).split())


def _staff_recipients():
    if settings.ENQUIRY_NOTIFY_EMAILS:
        return settings.ENQUIRY_NOTIFY_EMAILS
    raw = SiteSettings.load().notification_emails
    return [e.strip() for e in raw.split(",") if e.strip()]


def send_enquiry_notifications(enquiry):
    """Never raises: an email outage must not lose an enquiry."""
    recipients = _staff_recipients()
    if recipients:
        body = (
            f"New {enquiry.get_enquiry_type_display().lower()} received.\n\n"
            f"Name: {enquiry.name}\nEmail: {enquiry.email}\nPhone: {enquiry.phone}\n"
            f"Country: {enquiry.country_interest or '-'}\nLevel: {enquiry.get_study_level_display() or '-'}\n"
            f"Reference: {enquiry.reference}\n\nMessage:\n{enquiry.message or '-'}\n")
        try:
            send_mail(f"[Bhumi Pathways] New enquiry from {_one_line(enquiry.name)}", body,
                      settings.DEFAULT_FROM_EMAIL, recipients)
        except Exception:
            logger.exception("Staff notification failed for enquiry %s", enquiry.reference)
    if settings.ENQUIRY_SEND_ACKNOWLEDGEMENT:
        body = (
            f"Hello {_one_line(enquiry.name)},\n\n"
            "Thank you for contacting Bhumi Pathways Consultancy. We have received your enquiry and a "
            "counsellor will contact you using the details you provided.\n\n"
            f"Your reference: {enquiry.reference}\n\n"
            "This email is an acknowledgement only. It is not an offer of admission and does not guarantee "
            "any admission or visa outcome.\n\nBhumi Pathways Consultancy")
        try:
            send_mail("We have received your enquiry - Bhumi Pathways Consultancy", body,
                      settings.DEFAULT_FROM_EMAIL, [enquiry.email])
        except Exception:
            logger.exception("Acknowledgement failed for enquiry %s", enquiry.reference)
