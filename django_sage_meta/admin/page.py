from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.http import HttpResponseRedirect

from django_sage_meta.models import FacebookPageData
from django_sage_meta.repository import SyncService


@admin.register(FacebookPageData)
class FacebookPageDataAdmin(admin.ModelAdmin):
    save_on_top = True
    change_list_template = "admin/email/page.html"

    list_display = ("id", "page_id", "name", "category")
    search_fields = ("page_id", "name", "category")
    search_help_text = _("Search by Page ID, Name, or Category")
    list_filter = ("category",)
    ordering = ("id",)
    fieldsets = (
        ("Content", {"fields": ("page_id", "name", "access_token")}),
        (
            "Categories and Tasks",
            {"fields": ("category", "tasks"), "classes": ("collapse",)},
        ),
        (
            "Instagram Business Account",
            {"fields": ("instagram_business_account",), "classes": ("collapse",)},
        ),
    )
    autocomplete_fields = ["instagram_business_account"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync-page/",
                self.admin_site.admin_view(self.sync_insta_page),
                name="sync_page",
            )
        ]
        return custom_urls + urls

    def sync_insta_page(self, request):
        try:
            SyncService.sync_facebook_pages()
            self.message_user(request, _("Instagram pages synchronized successfully."))
            return HttpResponseRedirect("/admin/django_sage_meta/facebookpagedata")

        except Exception as e:
            self.message_user(request, _(f"An error occurred: {e}"), level="error")
