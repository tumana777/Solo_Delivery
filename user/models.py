from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from core.models import ChinaAddress, USAAddress
from user.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    first_name_ka = models.CharField(_('სახელი(ქართულად)'), max_length=30)
    last_name_ka = models.CharField(_('გვარი(ქართულად)'), max_length=50)
    first_name_en = models.CharField(_('სახელი(ლათინურად)'), max_length=30)
    last_name_en = models.CharField(_('გვარი(ლათინურად)'), max_length=50)
    email = models.EmailField(_('ელ.ფოსტა'),unique=True)
    balance = models.DecimalField(_('ბალანსი'), max_digits=12, decimal_places=2, default=0)
    personal_ID = models.CharField(
        _('პირადი ნომერი'),
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(r'^\d{11}$', 'არასწორი პირადი ნომერი')
        ]
    )
    address = models.CharField(_('მისამართი'), max_length=255)
    phone_number = models.CharField(
        _('მობილურის ნომერი'),
        max_length=9,
        validators=[
            RegexValidator(r'^\d{9}$', _('არასწორი მობილურის ნომერი'))
        ]
    )
    branch = models.ForeignKey('core.Branch', verbose_name=_('ფილიალი'), on_delete=models.SET_NULL, null=True)
    room_number = models.CharField(_('ოთახის ნომერი'), max_length=10, unique=True, editable=False)

    objects = CustomUserManager()

    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name_en} {self.last_name_en} - {self.room_number}"

    def save(self, *args, **kwargs):
        if not self.room_number:
            last_user = CustomUser.objects.filter(room_number__startswith="SD").order_by('room_number').last()
            if last_user:
                last_room_number = int(last_user.room_number[2:])
                self.room_number = f"SD{last_room_number + 1:05d}"
            else:
                self.room_number = "SD10001"
        super().save(*args, **kwargs)