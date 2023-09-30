from django.contrib import admin
from django.urls import reverse

from tougcomsys.models import (
    Article,
    ArticleEventdate,
    ArticlePlacement,
    Comment,
    Image,
    Menu,
    Menuitem,
    Placement,
    Page,
    ICal,
    BlockedIcalEvent,
    Subscription,
    FeedSource,
)

# ArticleImage,

import icalendar
import recurring_ical_events
import requests
from django.utils.html import format_html


class ArticleEventdateInline(admin.StackedInline):
    model = ArticleEventdate
    extra = 1


class ArticlePlacementInline(admin.StackedInline):
    model = ArticlePlacement
    extra = 1


class IcalInline(admin.StackedInline):
    model = ICal
    extra = 1


class FeedSourceInline(admin.StackedInline):
    model = FeedSource
    extra = 1


class MenuitemInline(admin.StackedInline):
    model = Menuitem
    extra = 1


class PlacementAdmin(admin.ModelAdmin):
    list_display = ("__str__", "place_number")
    inlines = [ArticlePlacementInline, IcalInline, FeedSourceInline]


admin.site.register(Placement, PlacementAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "headline",
        "draft_status",
    )
    ordering = list(Article._meta.ordering)
    prepopulated_fields = {"slug": ["headline"]}

    inlines = [
        ArticlePlacementInline,
        ArticleEventdateInline,
    ]
    # ArticleImageInline,

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial["author"] = request.user
        return initial


admin.site.register(Article, ArticleAdmin)

admin.site.register(Image)


class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuitemInline]


admin.site.register(Menu, MenuAdmin)


class MenuitemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "url")
    prepopulated_fields = {"sort_name": ["label"]}


admin.site.register(Menuitem, MenuitemAdmin)


class ICalAdmin(admin.ModelAdmin):
    readonly_fields = ["note", "ICaltext"]

    def note(self, instance):
        return "To prevent an event from displaying,  Copy a UUID from the text below and add it as a supressor.  To refresh the text, save after choosing URL."

    def ICaltext(self, instance):
        icaltext = requests.get(instance.url).text
        return icaltext


admin.site.register(ICal)


class BlockedIcalEventAdmin(admin.ModelAdmin):
    class Media:
        js = ["tougcomsys/tougshire_ical.js"]

    readonly_fields = [
        "note",
        "ICaltext",
    ]

    def note(self, instance):
        return "To prevent an external event from displaying,  Copy its UUID from the text below and add it as a supressor.  To refresh the text, save after choosing URL."

    def ICaltext(self, instance):
        return format_html(
            '<div id="id_ical_text">-</div><div id="id_ical_text_url">'
            + reverse("tougcomsys:ical_text")
            + "</div>"
        )


admin.site.register(BlockedIcalEvent, BlockedIcalEventAdmin)

admin.site.register(Page)

admin.site.register(Comment)

admin.site.register(Subscription)

admin.site.register(FeedSource)
