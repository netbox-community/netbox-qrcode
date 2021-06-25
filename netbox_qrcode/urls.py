from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.QRcodeDeviceView.as_view(), name='qrcode_devices'),
    path('racks/', views.QRcodeRackView.as_view(), name='qrcode_racks'),
    path('cables/', views.QRcodeCableView.as_view(), name='qrcode_cables'),

    path('devices/print/', views.PrintView.as_view(), name='print_menu'),
    path('racks/print/', views.PrintView.as_view(), name='print_menu'),
    path('cables/print/', views.PrintView.as_view(), name='print_menu'),
]