from django.contrib import admin

# from tougcomsys.models import Event, EventDate, Image, Page, Placement, Post
from tougcomsys.models import Article, ArticleEventdate, ArticleImage, ArticlePlacement, Image, Placement

class ArticleEventdateInline(admin.StackedInline):
    model=ArticleEventdate
    exta=1

class ArticlePlacementInline(admin.StackedInline):
    model=ArticlePlacement
    exta=1

class ArticleImageInline(admin.StackedInline):
    model=ArticleImage
    exta=1


class PlacementAdmin(admin.ModelAdmin):
    list_display = ('title', 'place_number')
    inlines = [ArticlePlacementInline]

admin.site.register(Placement, PlacementAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('headline', 'slug', 'draft_status', 'sortable_date',  )
    ordering = list(Article._meta.ordering)
    prepopulated_fields={'slug': ["headline"]}

    inlines = [ArticleImageInline, ArticleEventdateInline, ArticlePlacementInline]

    def get_changeform_initial_data(self, request):

        initial = super().get_changeform_initial_data(request)
        initial['author'] = request.user
        return initial


admin.site.register(Article, ArticleAdmin)


admin.site.register(Image)
