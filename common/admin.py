from django.contrib import admin
from common.models.site import *


class NewsInline(admin.StackedInline):
    model = New
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_menu']
    readonly_fields =['slug']
    inlines = [NewsInline]



@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ['title', 'create', 'tags', 'views']
    list_filter = ['title', 'create', 'views']
    search_fields = ['title', 'short_desc', 'description']
    ordering = ['views', 'create']
    list_per_page = 5


    @admin.display(empty_value='???')
    def short_title(self, obj, *args, **kwargs) :
         return obj.title.split()[:2]

    @admin.display(empty_value='???')
    def tag(self, obj, *args, **kwargs):
        if obj.tags :
             return obj.tags.replace('#', '').title().split()[:2]

    @admin.display(boolean=True, description='Is Read')
    def is_read(self, obj):
        return obj.is_read



admin.site.register(Comment)
admin.site.register(Subscribe)
admin.site.register(Contact)