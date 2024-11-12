from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from .models import Location
from .serializers import LocationSerializer ,LocationSerializerss
from geopy.geocoders import Nominatim

class SaveLocationView(APIView):
    def post(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        country = request.data.get('country')
        state = request.data.get('state')
        district = request.data.get('district')
        city = request.data.get('city')

        if latitude is None or longitude is None:
            return Response({'error': 'Latitude and longitude are required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LocationSerializer(data={
            'latitude': latitude,
            'longitude': longitude,
            'country': country,
            'state': state,
            'district': district,
            'city': city
        })

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Location saved successfully!'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetLocationsView(APIView):
    def get(self, request):
        locations = Location.objects.all()
        geolocator = Nominatim(user_agent="geoapiExercises")
        result = []

        for location in locations:
            lat = location.point.y
            lng = location.point.x
            # Reverse geocoding to get the location name
            try:
                location_name = geolocator.reverse((lat, lng), language='en').address
            except Exception as e:
                location_name = "Unknown Location"
            result.append({
                'name': location_name,
                'point': {
                    'type': 'Point',
                    'coordinates': [lng, lat]
                }
            })

        return Response(result)


# to search querry location as per locationpy
class SearchLocationsView(APIView):
    def get(self, request):
        country = request.query_params.get('country')
        state = request.query_params.get('state')
        district = request.query_params.get('district')
        city = request.query_params.get('city')

        locations = Location.objects.all()

        if country:
            locations = locations.filter(country=country)
        if state:
            locations = locations.filter(state=state)
        if district:
            locations = locations.filter(district=district)
        if city:
            locations = locations.filter(city=city)

        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)



# to get latlong through on click on map
class LocationCreateView(APIView):
    def post(self, request):
        serializer = LocationSerializerss(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
