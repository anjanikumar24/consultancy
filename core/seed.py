import logging

from django.db import DatabaseError

from . import defaults

logger = logging.getLogger(__name__)


def seed_defaults(sender=None, **kwargs):
    """Create starter content after `migrate`. Lists are only seeded once, so deleting items in the admin sticks."""
    from .models import (FAQ, Destination, MenuItem, PageContent, Principle, ProcessStep, Service,
                         SiteSettings, VisaDocument)
    try:
        site = SiteSettings.load()
        for slug, data in defaults.PAGES.items():
            PageContent.objects.get_or_create(slug=slug, defaults=data)
        if site.seeded:
            return
        for i, (loc, label, url) in enumerate(defaults.MENU):
            MenuItem.objects.create(location=loc, label=label, url=url, order=i)
        for i, d in enumerate(defaults.DESTINATIONS):
            Destination.objects.create(order=i, **d)
        for i, (t, x) in enumerate(defaults.SERVICES):
            Service.objects.create(order=i, title=t, text=x)
        for i, (t, x) in enumerate(defaults.STEPS):
            ProcessStep.objects.create(order=i, title=t, text=x)
        for i, (t, x) in enumerate(defaults.PRINCIPLES):
            Principle.objects.create(order=i, title=t, text=x)
        for i, t in enumerate(defaults.VISA_DOCS):
            VisaDocument.objects.create(order=i, text=t)
        for i, (q, a) in enumerate(defaults.FAQS):
            FAQ.objects.create(order=i, question=q, answer=a)
        site.seeded = True
        site.save(update_fields=["seeded"])
    except DatabaseError:
        logger.warning("Could not seed default content. Run `python manage.py makemigrations core` then `migrate`.")
