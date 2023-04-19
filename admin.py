from django.contrib import admin

from tougcomsys.models import Event, EventDate, Image, Page, Placement, Post

class PlacementAdmin(admin.ModelAdmin):
    list_display = ('title', 'place_number')

admin.site.register(Placement, PlacementAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'draft_status', 'placement', )
    ordering = ['placement'] + list(Post._meta.ordering)
    prepopulated_fields={'slug': ["title"]}

    def get_changeform_initial_data(self, request):

        initial = super().get_changeform_initial_data(request)
        initial['author'] = request.user
        return initial


admin.site.register(Post, PostAdmin)

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'draft_status')

    prepopulated_fields={'slug': ["title"]}


admin.site.register(Page, PageAdmin)

class EventDateInline(admin.StackedInline):
    model=EventDate
    exta=5

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'draft_status')
    inlines = [EventDateInline,]

    prepopulated_fields={'slug': ["title"]}


admin.site.register(Event, EventAdmin)


admin.site.register(EventDate)

admin.site.register(Image)
