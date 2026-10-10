import csv

from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from .models import (FAQ, Destination, Enquiry, MenuItem, PageContent, Principle, ProcessStep, Service,
                     SiteSettings, VisaDocument)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Brand", {"fields": ["site_name", "tagline", "announcement_text", "cta_label"]}),
        ("Contact details (shown in header, footer and Contact page)",
         {"fields": ["phone", "email", "whatsapp_number", "whatsapp_message", "address", "office_hours"]}),
        ("Footer and search engines", {"fields": ["footer_about", "default_meta_description"]}),
        ("Enquiry alerts", {"fields": ["notification_emails"]}),
        ("Home page section headings", {"fields": [
            "home_destinations_title", "home_destinations_intro", "home_services_title", "home_services_intro",
            "home_steps_title", "home_cta_title", "home_cta_text"]}),
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):  # single row: go straight to the form
        obj = SiteSettings.load()
        return redirect(reverse("admin:core_sitesettings_change", args=[obj.pk]))


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "hero_title", "seo_title")
    readonly_fields = ("slug",)
    fieldsets = [
        (None, {"fields": ["slug"]}),
        ("Search engines", {"fields": ["seo_title", "meta_description"]}),
        ("Top banner", {"fields": ["eyebrow", "hero_title", "hero_text"]}),
        ("Page content", {"fields": ["body", "section_title", "section_intro", "notice"]}),
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OrderableAdmin(admin.ModelAdmin):
    list_editable = ("order", "is_active")


@admin.register(MenuItem)
class MenuItemAdmin(OrderableAdmin):
    list_display = ("label", "location", "url", "order", "is_active")
    list_filter = ("location",)


@admin.register(Destination)
class DestinationAdmin(OrderableAdmin):
    list_display = ("name", "flag", "intakes", "order", "is_active")


@admin.register(Service)
class ServiceAdmin(OrderableAdmin):
    list_display = ("title", "order", "is_active")


@admin.register(ProcessStep)
class ProcessStepAdmin(OrderableAdmin):
    list_display = ("title", "order", "is_active")


@admin.register(Principle)
class PrincipleAdmin(OrderableAdmin):
    list_display = ("title", "order", "is_active")


@admin.register(VisaDocument)
class VisaDocumentAdmin(OrderableAdmin):
    list_display = ("text", "order", "is_active")


@admin.register(FAQ)
class FAQAdmin(OrderableAdmin):
    list_display = ("question", "order", "is_active")


def _safe(value):
    s = str(value)
    return "'" + s if s[:1] in "=+-@\t\r" else s  # block spreadsheet formula injection


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "enquiry_type", "country_interest", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "enquiry_type", "country_interest")
    search_fields = ("name", "email", "phone")
    date_hierarchy = "created_at"
    readonly_fields = ("reference", "name", "email", "phone", "enquiry_type", "country_interest",
                       "study_level", "message", "consent", "created_at", "updated_at")
    fields = readonly_fields + ("status", "admin_notes")
    actions = ["mark_contacted", "mark_in_progress", "mark_closed", "export_csv"]

    def has_add_permission(self, request):
        return False

    @admin.action(description="Mark selected as Contacted")
    def mark_contacted(self, request, queryset):
        queryset.update(status=Enquiry.Status.CONTACTED)

    @admin.action(description="Mark selected as In progress")
    def mark_in_progress(self, request, queryset):
        queryset.update(status=Enquiry.Status.IN_PROGRESS)

    @admin.action(description="Mark selected as Closed")
    def mark_closed(self, request, queryset):
        queryset.update(status=Enquiry.Status.CLOSED)

    @admin.action(description="Export selected to CSV")
    def export_csv(self, request, queryset):
        resp = HttpResponse(content_type="text/csv")
        resp["Content-Disposition"] = 'attachment; filename="enquiries.csv"'
        w = csv.writer(resp)
        w.writerow(["Date", "Name", "Email", "Phone", "Type", "Country", "Level", "Status", "Message", "Notes"])
        for e in queryset:
            w.writerow([_safe(x) for x in (e.created_at.strftime("%Y-%m-%d %H:%M"), e.name, e.email, e.phone,
                                           e.get_enquiry_type_display(), e.country_interest,
                                           e.get_study_level_display(), e.get_status_display(), e.message, e.admin_notes)])
        return resp
