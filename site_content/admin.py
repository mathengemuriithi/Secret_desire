from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import (FAQ, ContactMessage, GalleryImage, Package, Service,
                     SiteSettings, TeamMember, Testimonial)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.get_solo()
        return redirect(reverse("admin:site_content_sitesettings_change", args=[obj.pk]))


class OrderedAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)


@admin.register(Service)
class ServiceAdmin(OrderedAdmin):
    list_display = ("name", "duration", "price", "order", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Package)
class PackageAdmin(OrderedAdmin):
    list_display = ("name", "duration", "price", "order", "is_active")


@admin.register(Testimonial)
class TestimonialAdmin(OrderedAdmin):
    list_display = ("name", "order", "is_active")


@admin.register(TeamMember)
class TeamMemberAdmin(OrderedAdmin):
    list_display = ("name", "role", "order", "is_active")


@admin.register(GalleryImage)
class GalleryImageAdmin(OrderedAdmin):
    list_display = ("__str__", "category", "order", "is_active")
    list_filter = ("is_active", "category")


@admin.register(FAQ)
class FAQAdmin(OrderedAdmin):
    list_display = ("question", "order", "is_active")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "created_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
