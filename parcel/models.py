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
    online_store = models.CharField(_('ონლაინ მაღაზია'), blank=True, max_length=100)
    branch = models.ForeignKey('core.Branch', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('ფილიალი'))
    status = models.ForeignKey('core.Status', on_delete=models.SET_NULL, null=True, verbose_name=_('სტატუსი'))
    delivery_time = models.DateField(_('ჩაბარების თარიღი'), auto_now_add=True)
    taken_time = models.DateField(_('გატანის თარიღი'), blank=True, null=True)
    weight = models.DecimalField(_('წონა'), max_digits=5, decimal_places=2, null=True)
    custom_clearance = models.BooleanField(_('განბაჟება'), default=False)
    is_paid = models.BooleanField(_('გადახდილია'), default=False)
    is_declared = models.BooleanField(_('დეკლარირებულია'), default=False)
    transporting_fee = models.DecimalField(max_digits=5, decimal_places=2, editable=False, verbose_name=_('ტრ. საფასური'))

    class Meta:
        verbose_name = _('ამანათი')
        verbose_name_plural = _('ამანათები')

    def __str__(self):
        return self.tracking_number

    def save(self, *args, **kwargs):
        if not self.branch:
            self.branch = self.user.branch

        if not self.transporting_fee:
            self.transporting_fee = self.weight * self.country.transporting_price

        if self.category and self.price and self.currency and self.online_store:
            self.is_declared = True
        else:
            self.is_declared = False

        super().save(*args, **kwargs)