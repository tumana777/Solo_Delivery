from django.db import models
from django.utils.translation import gettext_lazy as _

class Country(models.Model):
    name = models.CharField(_('სახელი'), max_length=255)
    code = models.CharField(_("კოდი"), max_length=2, unique=True)
    transporting_price = models.DecimalField(_('ტრანსპორტირების ფასი'), decimal_places=2, max_digits=4, null=True, blank=True)

    class Meta:
        verbose_name = _('ქვეყანა')
        verbose_name_plural = _('ქვეყნები')

    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(_('დასახელება'), max_length=255)

    class Meta:
        verbose_name = _('ვალუტა')
        verbose_name_plural = _('ვალუტები')

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(_('სტატუსი'), max_length=255)

    class Meta:
        verbose_name_plural = _('სტატუსი')

    def __str__(self):
        return self.name

class Flight(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, verbose_name=_('სტატუსი'))
    departure_date = models.DateField(_("გამოფრენის თარიღი"), auto_now_add=True)
    estimated_arrival_date = models.DateField(_("ჩამოფრენის სავარაუდო თარიღი"))
    arrival_date = models.DateField(_("ჩამოფრენის თარიღი"), null=True, blank=True)
    flight_number = models.CharField(_("რეისის ნომერი"), max_length=10, unique=True, editable=False)

    class Meta:
        verbose_name = _("რეისი")
        verbose_name_plural = _("რეისები")

    def __str__(self):
        return self.flight_number

    def save(self, *args, **kwargs):
        if not self.flight_number:
            country_code = self.country.code.upper()
            last_flight = Flight.objects.filter(country=self.country).order_by('-id').first()
            next_number = 1 if not last_flight else int(last_flight.flight_number[2:]) + 1
            self.flight_number = f"{country_code}{next_number:05d}"

        if not self.pk and not self.status:
            self.status = Status.objects.get(name="გზაშია")

        super().save(*args, **kwargs)

class Branch(models.Model):
    name = models.CharField(_('სახელი'), max_length=100)
    address = models.CharField(_('მისამართი'), max_length=100)

    class Meta:
        verbose_name = _('ფილიალი')
        verbose_name_plural = _('ფილიალები')

    def __str__(self):
        return self.name

class ChinaAddress(models.Model):
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
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
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
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