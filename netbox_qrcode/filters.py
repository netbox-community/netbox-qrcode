import django_filters
from django.db import models

from dcim.models import Site, Region, Rack, Manufacturer, RackRole
from dcim.choices import DeviceStatusChoices, RackStatusChoices

from utilities.filters import TreeNodeMultipleChoiceFilter

from .models import QRExtendedDevice, QRExtendedRack, QRExtendedCable

class BaseFiltersSet(django_filters.FilterSet):

    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    region = TreeNodeMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='site__region',
        lookup_expr='in',
        to_field_name='slug',
        label='Region (slug)',
    )
    site = django_filters.ModelMultipleChoiceFilter(
        field_name='site__slug',
        queryset=Site.objects.all(),
        to_field_name='slug',
        label='Site name (slug)',
    )

# Recieves QuerySet in Views.py and filters based on form values, returns the resulting filtered queryset back to views.py
class SearchDeviceFilterSet(BaseFiltersSet):

    status = django_filters.MultipleChoiceFilter(
        choices=DeviceStatusChoices,
        null_value=None
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        queryset= QRExtendedDevice.objects.all(),
        to_field_name='id',
        field_name='id',
        label='Device (ID)',
    )
    rack_id = django_filters.ModelMultipleChoiceFilter(
        field_name='rack',
        queryset=Rack.objects.all(),
        label='Rack (ID)',
    )
    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type__manufacturer__slug',
        queryset=Manufacturer.objects.all(),
        to_field_name='slug',
        label='Manufacturer (slug)',
    )

    class Meta:
        model = QRExtendedDevice
        fields = ['id', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            models.Q(name__icontains=value)
        )

class SearchRackFilterSet(BaseFiltersSet):

    status = django_filters.MultipleChoiceFilter(
        choices=RackStatusChoices,
        null_value=None
    )
    role = django_filters.ModelMultipleChoiceFilter(
        field_name='role__slug',
        queryset=RackRole.objects.all(),
        to_field_name='slug',
        label='Role (slug)',
    )

    class Meta:
        model = QRExtendedRack
        fields = ['id', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            models.Q(name__icontains=value)
        )

class SearchCableFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    
    class Meta:
        model = QRExtendedCable
        fields = ['id', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(label__icontains=value)

    def filter_device(self, queryset, name, value):
        queryset = queryset.filter(
            models.Q(**{'_termination_a_{}__in'.format(name): value}) |
            models.Q(**{'_termination_b_{}__in'.format(name): value})
        )
        return queryset




