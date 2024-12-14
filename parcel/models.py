from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(_("დასახელება"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("კატეგორია")
        verbose_name_plural = _("კატეგორიები")

    def __str__(self):
        return self.name

class Parcel(models.Model):
    tracking_number = models.CharField(_("თრექინგი"), max_length=100, unique=True)
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, verbose_name=_('მომხმარებელი'))
    flight = models.ForeignKey('core.Flight', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('რეისი'))
    country = models.ForeignKey('core.Country', on_delete=models.SET_NULL, null=True, verbose_name=_('ქვეყანა'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('კატეგორია'))
    price = models.DecimalField(_('ფასი'),null=True, blank=True, max_digits=10, decimal_places=2)
    currency = models.ForeignKey('core.Currency', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('ვალუტა'))
    branch = models.ForeignKey('core.Branch', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('ფილიალი'))
    status = models.ForeignKey('core.Status', on_delete=models.SET_NULL, null=True, verbose_name=_('სტატუსი'))
    online_store = models.CharField(_('ონლაინ მაღაზია'), blank=True, max_length=100)
    delivery_time = models.DateField(_('ჩაბარების თარიღი'))
    taken_time = models.DateField(_('გატანის თარიღი'), blank=True, null=True)
    weight = models.DecimalField(_('წონა'), max_digits=5, decimal_places=2, null=True)
    custom_clearance = models.BooleanField(_('განბაჟება'), default=False)
    is_paid = models.BooleanField(_('გადახდილია'), default=False)
    transporting_fee = models.DecimalField(_('ტრანსპორტირების საფასური'), max_digits=5, decimal_places=2, editable=False)

    class Meta:
        verbose_name = _('ამანათი')
        verbose_name_plural = _('ამანათები')

    def __str__(self):
        return self.tracking_number

    def save(self, *args, **kwargs):
        if not self.transporting_fee:
            self.transporting_fee = self.weight * self.country.transporting_price

        super().save(*args, **kwargs)