from rest_framework import serializers
from marketplace.models import Energy, Energy_Type, EnergyOffer


class EnergyTypeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Energy_Type
        fields = '__all__'

class EnergyTypeUpdateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Energy_Type
        fields = '__all__'
        read_only_fields = ['id', 'created_on']


class EnergySerializers(serializers.ModelSerializer):

    class Meta:
        model = Energy
        fields = '__all__'

class EnergyUpdateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Energy
        fields = '__all__'
        read_only_fields = ['seller_id', 'created_on', 'energy_type']


class EnergyOfferSerializers(serializers.ModelSerializer):

    class Meta:
        model = EnergyOffer
        fields = '__all__'
