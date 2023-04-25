from django.contrib import admin

# from tougcomsys.models import Event, EventDate, Image, Page, Placement, Post
from tougcomsys.models import Article, ArticleEventdate, ArticleImage, ArticlePlacement, Image, Menu, MenuLink, Menuitem, Placement

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

    def get_changeform_initial_data(self, request):

        initial = super().get_changeform_initial_data(request)

        print('tp234od21', self.get_formsets_with_inlines(request))
        
        return initial


admin.site.register(Menu, MenuAdmin)

admin.site.register(MenuLink)

admin.site.register(Menuitem)