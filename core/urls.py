from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("destinations/", views.destinations, name="destinations"),
    path("visa-assistance/", views.visa, name="visa"),
    path("faqs/", views.faqs, name="faqs"),
    path("contact/", views.contact, name="contact"),
    path("contact/thank-you/", views.thanks, name="thanks"),
    path("privacy-policy/", views.legal, {"slug": "privacy"}, name="privacy"),
    path("terms/", views.legal, {"slug": "terms"}, name="terms"),
]
