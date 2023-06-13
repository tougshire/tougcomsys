from django.contrib import admin

# from tougcomsys.models import Event, EventDate, Image, Page, Placement, Post
from tougcomsys.models import Article, ArticleEventdate, ArticleImage, ArticlePlacement, Image, Menu, MenuLink, Menuitem, Placement, ICal, BlockedIcalEvent

from ics import Calendar
import requests

class ArticleEventdateInline(admin.StackedInline):
    model=ArticleEventdate
    extra=1

class ArticlePlacementInline(admin.StackedInline):
    model=ArticlePlacement
    extra=1

class ArticleImageInline(admin.StackedInline):
    model=ArticleImage
    extra=1

class MenuitemInline(admin.StackedInline):
    model=Menuitem
    extra=1

class PlacementAdmin(admin.ModelAdmin):
    list_display = ('title', 'place_number')
    inlines = [ArticlePlacementInline]

admin.site.register(Placement, PlacementAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('headline', 'slug', 'draft_status', 'sortable_date',  )
    ordering = list(Article._meta.ordering)
    prepopulated_fields={'slug': ["headline"]}

    inlines = [ArticlePlacementInline, ArticleImageInline, ArticleEventdateInline, ]

    def get_changeform_initial_data(self, request):

        initial = super().get_changeform_initial_data(request)
        initial['author'] = request.user
        return initial


admin.site.register(Article, ArticleAdmin)

admin.site.register(Image)

class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuitemInline]
    prepopulated_fields={'sort_name': ['name']}

admin.site.register(Menu, MenuAdmin)

admin.site.register(MenuLink)

class MenuitemAdmin(admin.ModelAdmin):

    prepopulated_fields={'sort_name': ['label']}

admin.site.register(Menuitem, MenuitemAdmin)

class ICalAdmin(admin.ModelAdmin):

    readonly_fields = [ 'note', 'ICaltext' ]

    def note( self, instance ):
        return 'To prevent an event from displaying,  Copy a UUID from the text below and add it as a supressor.  To refresh the text, save after choosing URL.'

    def ICaltext( self, instance ):
        
        icaltext = requests.get( instance.url ).text
        return icaltext

admin.site.register(ICal, ICalAdmin)

admin.site.register(BlockedIcalEvent)