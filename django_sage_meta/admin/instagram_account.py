from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path

from django_sage_meta.repository import SyncService
from django_sage_meta.models import InstagramAccount


@admin.register(InstagramAccount)
class InstagramAccountAdmin(admin.ModelAdmin):
    save_on_top = True
    change_list_template = "admin/email/insta.html"
    list_display = (
        "id",
        "account_id",
        "username",
        "followers_counts",
        "follows_counts",
    )
    search_fields = ("account_id", "username", "biography")
    search_help_text = _("Search by Account ID, Username, or Biography")
    list_filter = ("followers_counts", "follows_counts", "media_counts")
    ordering = ("id",)
    fieldsets = (
        (
            "Content",
            {
                "fields": (
                    "account_id",
                    "username",
                    "follows_counts",
                    "followers_counts",
                    "media_counts",
                    "profile_picture_url",
                    "website",
                    "biography",
                )
            },
        ),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync-insta/",
                self.admin_site.admin_view(self.sync_insta_business),
                name="sync_insta",
            )
        ]
        return custom_urls + urls

    def sync_insta_business(self, request):
        try:
            SyncService.sync_instagram_accounts()
            self.message_user(
                request, _("Instagram accounts synchronized successfully.")
            )
            return HttpResponseRedirect("admin/django_sage_meta/instagramaccount/")
        except Exception as e:
            self.message_user(request, _(f"An error occurred: {e}"), level="error")
            return HttpResponse(f"An error occurred: {e}", status=500)
