from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Location ,maplocation


class LocationSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    point = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['point', 'latitude', 'longitude', 'country', 'state', 'district', 'city']

    def get_point(self, obj):
        return {
            'type': 'Point',
            'coordinates': [obj.point.x, obj.point.y]
        }

    def validate(self, attrs):
        latitude = attrs.get('latitude')
        longitude = attrs.get('longitude')

        if latitude is None or longitude is None:
            raise serializers.ValidationError("Latitude and longitude are required.")

        if not (-90 <= latitude <= 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        if not (-180 <= longitude <= 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180.")

        return attrs

    def create(self, validated_data):
        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')

        point = Point(x=longitude, y=latitude)
        location = Location.objects.create(point=point, **validated_data)

        return location


class LocationSerializerss(serializers.ModelSerializer):
    # Handle the location field directly as GeoJSON
    location = serializers.JSONField()

    class Meta:
        model = maplocation
        fields = ['location']

    def validate_location(self, value):
        """
        Validate the GeoJSON location field to ensure it's a valid Point.
        """
        if value.get('type') != 'Point':
            raise serializers.ValidationError("Invalid location type. Expected 'Point'.")

        if not isinstance(value.get('coordinates'), list) or len(value['coordinates']) != 2:
            raise serializers.ValidationError("Invalid coordinates. Expected a list with [longitude, latitude].")

        return value

    def create(self, validated_data):
        # Extract GeoJSON data from validated_data
        location_data = validated_data.get('location')
        coordinates = location_data.get('coordinates')
        lng, lat = coordinates[0], coordinates[1]  # GeoJSON format: [lng, lat]

        # Create a Point object using the extracted coordinates
        location_point = Point(lng, lat)

        # Save location to the maplocation model
        location = maplocation.objects.create(location=location_point)
        return location

    def to_representation(self, instance):
        """
        Customize the output format of the serialized object.
        """
        representation = super().to_representation(instance)
        representation['location'] = {
            'type': 'Point',
            'coordinates': [instance.location.x, instance.location.y],
        }
        return representation