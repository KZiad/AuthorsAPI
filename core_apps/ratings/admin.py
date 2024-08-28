from django.contrib import admin
from .models import Rating


class RatingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "article", "rating", "created_at", "updated_at"]
    list_display_links = ["id", "article"]


admin.site.register(Rating, RatingAdmin)
