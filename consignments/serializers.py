from rest_framework import serializers
from .models import Vendor
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import (
    Consignment, ConsignmentItem, ConsignmentItemSize,
    TransportDetails, FreightCharges, Vendor, LoadingPoint, UnloadingPoint
)



class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'address', 'gst']  # Exclude 'user'

class ConsignmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsignmentItem
        exclude = ['consignment']


class ConsignmentItemSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsignmentItemSize
        exclude = ['consignment']


class TransportDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportDetails
        exclude = ['consignment']


class FreightChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreightCharges
        exclude = ['consignment']


class LoadingPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadingPoint
        exclude = ['consignment']

class UnloadingPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnloadingPoint
        exclude = ['consignment']


class ConsignmentSerializer(WritableNestedModelSerializer):
    items = ConsignmentItemSerializer(many=True)
    sizes = ConsignmentItemSizeSerializer(many=True)
    transport_details = TransportDetailsSerializer()
    freight_charges = FreightChargesSerializer()
    unloading_point = UnloadingPointSerializer()
    loading_point = LoadingPointSerializer()
    consignor = VendorSerializer(read_only=True)
    consignee = VendorSerializer(read_only=True)
    consignor_id = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(), write_only=True, source='consignor'
    )
    consignee_id = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(), write_only=True, source='consignee'
    )


    class Meta:
        model = Consignment
        exclude = ['user']

    def create(self, validated_data):
        user = self.context['request'].user

        items_data = validated_data.pop('items')
        sizes_data = validated_data.pop('sizes')
        transport_data = validated_data.pop('transport_details')
        freight_data = validated_data.pop('freight_charges')
        unloading_point_data = validated_data.pop('unloading_point')
        loading_point_data = validated_data.pop('loading_point')

        consignment = Consignment.objects.create(user=user, **validated_data)

        for item in items_data:
            ConsignmentItem.objects.create(consignment=consignment, **item)

        for size in sizes_data:
            ConsignmentItemSize.objects.create(consignment=consignment, **size)

        TransportDetails.objects.create(consignment=consignment, **transport_data)
        FreightCharges.objects.create(consignment=consignment, **freight_data)
        UnloadingPoint.objects.create(consignment=consignment, **unloading_point_data)
        LoadingPoint.objects.create(consignment=consignment, **loading_point_data)

        return consignment
