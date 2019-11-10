from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class State(models.Model):
    """State from the court district"""
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    initials = models.CharField(max_length=2, null=False, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name=_('State'))

    def __str__(self):
        return self.name


class CourtDistrict(models.Model):
    """Court district object"""
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name=_('CourtDistrict'),
    )
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_('State'))

    def __str__(self):
        return self.name
