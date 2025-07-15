from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vendors")
    name = models.CharField(max_length=255)
    address = models.TextField()
    gst = models.TextField()

    def __str__(self):
        return self.name



class Consignment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="consignments"
    )
    
    consignment_note_no = models.CharField(max_length=255, unique=True)
    date = models.DateField(default=timezone.now)
    invoice_no = models.CharField(max_length=255)
    invoice_date = models.DateField()

    consignor = models.ForeignKey(
        Vendor, related_name="consignments_as_consignor",
        on_delete=models.CASCADE
    )
    consignee = models.ForeignKey(
        Vendor, related_name="consignments_as_consignee",
        on_delete=models.CASCADE
    )

    value = models.CharField(max_length=255)
    delivery_address = models.TextField()
    size_cft = models.FloatField()

    def __str__(self):
        return f"Consignment {self.consignment_note_no}"



class ConsignmentItem(models.Model):
    consignment = models.ForeignKey(
        Consignment, related_name="items",
        on_delete=models.CASCADE
    )

    no_of_packages = models.CharField(max_length=255)
    method_of_packing = models.CharField(max_length=255)
    description = models.TextField()
    weight_actual = models.FloatField()
    weight_charges = models.FloatField()

    def __str__(self):
        return f"Item for Consignment {self.consignment.consignment_note_no}"


class ConsignmentItemSize(models.Model):
    consignment = models.ForeignKey(
        Consignment, related_name="sizes",
        on_delete=models.CASCADE
    )

    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    extra = models.FloatField()

    def __str__(self):
        return f"Size for Consignment {self.consignment.consignment_note_no}"


class TransportDetails(models.Model):
    consignment = models.OneToOneField(
        Consignment, related_name="transport_details",
        on_delete=models.CASCADE
    )

    vehicle_no = models.CharField(max_length=255)
    driver_license_no = models.CharField(max_length=255)
    driver_name = models.CharField(max_length=255)
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255)
    e_way_bill_no = models.CharField(max_length=255)

    def __str__(self):
        return f"Transport for {self.consignment.consignment_note_no}"


class FreightCharges(models.Model):
    consignment = models.OneToOneField(
        Consignment, related_name="freight_charges",
        on_delete=models.CASCADE
    )

    freight = models.FloatField()
    advance = models.FloatField()
    hamali = models.FloatField()
    extra = models.FloatField()
    st_charges = models.FloatField()
    total = models.FloatField()
    gst = models.FloatField()

    def __str__(self):
        return f"Freight Charges for {self.consignment.consignment_note_no}"
