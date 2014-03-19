from django.contrib import admin
from polls.models import News, Text

class TextInline(admin.TabularInline):
    model = Text
    extra = 3

class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [TextInline]
    list_display = ('title', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['title']

admin.site.register(News, NewsAdmin)
