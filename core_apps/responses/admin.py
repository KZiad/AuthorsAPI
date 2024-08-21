from django.contrib import admin
from .models import Response


class ResponseAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "article"]
    list_display_links = ["id", "user", "article"]


admin.site.register(Response, ResponseAdmin)
