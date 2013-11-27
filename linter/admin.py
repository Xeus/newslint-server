from django.contrib import admin
from linter.models import Clipping


class ClippingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'content']}),
        ('Source', {'fields': ['publication', 'author', 'url']}),
        ('Dates', {'fields': ['published']})
    ]


admin.site.register(Clipping, ClippingAdmin)
