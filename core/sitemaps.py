from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return ["home", "about", "services", "destinations", "visa", "faqs", "contact", "privacy", "terms"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "home" else 0.7
