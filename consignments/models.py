from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vendors", null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    gst = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name or "Vendor"


class Consignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="consignments", null=True, blank=True)
    
    consignment_note_no = models.CharField(max_length=255, unique=True, null=True, blank=True)
    service_category = models.CharField(max_length=255, null=True, blank=True)
    person_liable_for_gst = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)
    invoice_no = models.CharField(max_length=255, null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)

    consignor = models.ForeignKey(Vendor, related_name="consignments_as_consignor", on_delete=models.CASCADE, null=True, blank=True)
    consignee = models.ForeignKey(Vendor, related_name="consignments_as_consignee", on_delete=models.CASCADE, null=True, blank=True)

    value = models.CharField(max_length=255, null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    size_cft = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Consignment {self.consignment_note_no or 'N/A'}"


class ConsignmentItem(models.Model):
    consignment = models.ForeignKey(Consignment, related_name="items", on_delete=models.CASCADE, null=True, blank=True)

    no_of_packages = models.CharField(max_length=255, null=True, blank=True)
    method_of_packing = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    weight_actual = models.FloatField(null=True, blank=True)
    weight_charges = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Item for Consignment {self.consignment.consignment_note_no if self.consignment else 'N/A'}"


class ConsignmentItemSize(models.Model):
    consignment = models.ForeignKey(Consignment, related_name="sizes", on_delete=models.CASCADE, null=True, blank=True)

    length = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    extra = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Size for Consignment {self.consignment.consignment_note_no if self.consignment else 'N/A'}"


class TransportDetails(models.Model):
    consignment = models.OneToOneField(Consignment, related_name="transport_details", on_delete=models.CASCADE, null=True, blank=True)

    vehicle_no = models.CharField(max_length=255, null=True, blank=True)
    vehicle_type = models.CharField(max_length=255, null=True, blank=True)
    driver_number = models.CharField(max_length=255, null=True, blank=True)
    driver_license_no = models.CharField(max_length=255, null=True, blank=True)
    driver_name = models.CharField(max_length=255, null=True, blank=True)
    from_location = models.CharField(max_length=255, null=True, blank=True)
    to_location = models.CharField(max_length=255, null=True, blank=True)
    e_way_bill_no = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Transport for {self.consignment.consignment_note_no if self.consignment else 'N/A'}"


class FreightCharges(models.Model):
    consignment = models.OneToOneField(Consignment, related_name="freight_charges", on_delete=models.CASCADE, null=True, blank=True)

    freight = models.FloatField(null=True, blank=True)
    advance = models.FloatField(null=True, blank=True)
    other_charges = models.FloatField(null=True, blank=True)
    st_charges = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Freight Charges for {self.consignment.consignment_note_no if self.consignment else 'N/A'}"


class LoadingPoint(models.Model):
    consignment = models.OneToOneField(Consignment, related_name="loading_point", on_delete=models.CASCADE, null=True, blank=True)

    in_time = models.TextField(null=True, blank=True)
    in_date = models.TextField(null=True, blank=True)
    out_time = models.TextField(null=True, blank=True)
    out_date = models.TextField(null=True, blank=True)


class UnloadingPoint(models.Model):
    consignment = models.OneToOneField(Consignment, related_name="unloading_point", on_delete=models.CASCADE, null=True, blank=True)

    in_time = models.TextField(null=True, blank=True)
    in_date = models.TextField(null=True, blank=True)
    out_time = models.TextField(null=True, blank=True)
    out_date = models.TextField(null=True, blank=True)
