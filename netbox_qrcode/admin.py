from django.contrib import admin
from .models import QRExtendedDevice, QRExtendedRack, QRExtendedCable

@admin.register(QRExtendedDevice)
class QRExtendedDeviceAdmin(admin.ModelAdmin):
    list_display = ("device", "photo")

@admin.register(QRExtendedRack)
class QRExtendedRackAdmin(admin.ModelAdmin):
    list_display = ("rack", "photo")

@admin.register(QRExtendedCable)
class QRExtendedCableAdmin(admin.ModelAdmin):
    list_display = ("cable", "photo")
