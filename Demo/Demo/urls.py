
from django.contrib import admin
from django.urls import path

from demoapp.views import SaveLocationView, GetLocationsView,SearchLocationsView ,LocationCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('save-location/', SaveLocationView.as_view(), name='save-location'),
    path('get-locations/', GetLocationsView.as_view(), name='get-locations'),
    path('search-locations/', SearchLocationsView.as_view(), name='search-locations'),
    path('locations/new/', LocationCreateView.as_view(), name='location-create'),

]
