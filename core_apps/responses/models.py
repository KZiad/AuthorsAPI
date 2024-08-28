from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import get_user_model
from core_apps.articles.models import Article
from core_apps.common.models import TimeStampedModel
User = get_user_model()


class Response(TimeStampedModel):
    user = models.ForeignKey(User, related_name="responses", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="responses", on_delete=models.CASCADE)
    parent_response = models.ForeignKey("self", related_name="replies", on_delete=models.CASCADE, blank=True, null=True)

    body = models.TextField(_("Response Content"))

    class Meta:
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.first_name} responded '{self.body[:20]}'"
