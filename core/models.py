from django.db import models
from django.utils.translation import gettext_lazy as _

class Branch(models.Model):
    name = models.CharField(_('სახელი'), max_length=100)
    address = models.CharField(_('მისამართი'), max_length=100)

    class Meta:
        verbose_name = _('ფილიალი')
        verbose_name_plural = _('ფილიალები')

    def __str__(self):
        return self.name

class ChinaAddress(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    cell_phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = _('ჩინეთის მისამართი')
        verbose_name_plural = _('ჩინეთის მისამართი')

    def __str__(self):
        return f"{self.city}, {self.province}"


class USAAddress(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)
    address_1 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    cell_phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = _('ამერიკის მისამართი')
        verbose_name_plural = _('ამერიკის მისამართი')

    def __str__(self):
        return f"{self.city}, {self.state}"