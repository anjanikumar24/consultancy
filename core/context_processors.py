from datetime import date

from .models import MenuItem, SiteSettings


def site(request):
    s = SiteSettings.load()
    items = list(MenuItem.objects.filter(is_active=True))
    return {
        "site": s,
        "header_menu": [i for i in items if i.location == "header"],
        "footer_menu": [i for i in items if i.location == "footer"],
        "legal_menu": [i for i in items if i.location == "legal"],
        "canonical_url": request.build_absolute_uri(request.path),
        "current_year": date.today().year,
    }
