from django.contrib import admin
from .models import (
    Vendor, Consignment, ConsignmentItem, ConsignmentItemSize,
    TransportDetails, FreightCharges
)

# Inline for ConsignmentItem
class ConsignmentItemInline(admin.TabularInline):
    model = ConsignmentItem
    extra = 1

# Inline for ConsignmentItemSize
class ConsignmentItemSizeInline(admin.TabularInline):
    model = ConsignmentItemSize
    extra = 1

# Inline for TransportDetails (OneToOne)
class TransportDetailsInline(admin.StackedInline):
    model = TransportDetails
    extra = 0
    max_num = 1

# Inline for FreightCharges (OneToOne)
class FreightChargesInline(admin.StackedInline):
    model = FreightCharges
    extra = 0
    max_num = 1


# Consignment Admin
@admin.register(Consignment)
class ConsignmentAdmin(admin.ModelAdmin):
    list_display = ('consignment_note_no', 'user', 'consignor', 'consignee', 'date')
    inlines = [ConsignmentItemInline, ConsignmentItemSizeInline, TransportDetailsInline, FreightChargesInline]
    search_fields = ['consignment_note_no', 'invoice_no']
    list_filter = ['date', 'user']


# Vendor Admin
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'gst', 'user')
    search_fields = ['name', 'gst']
    list_filter = ['user']


# Optional (if needed to register directly)
@admin.register(ConsignmentItem)
class ConsignmentItemAdmin(admin.ModelAdmin):
    list_display = ('consignment', 'no_of_packages', 'weight_actual')
    search_fields = ['description']
    list_filter = ['consignment']


@admin.register(ConsignmentItemSize)
class ConsignmentItemSizeAdmin(admin.ModelAdmin):
    list_display = ('consignment', 'length', 'width', 'height', 'extra')


@admin.register(TransportDetails)
class TransportDetailsAdmin(admin.ModelAdmin):
    list_display = ('consignment', 'vehicle_no', 'driver_name', 'from_location', 'to_location')


@admin.register(FreightCharges)
class FreightChargesAdmin(admin.ModelAdmin):
    list_display = ('consignment', 'freight', 'total', 'gst')
