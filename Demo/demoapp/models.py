
from django.contrib.gis.db import models

class Location(models.Model):
    point = models.PointField()
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Location ({self.point.x}, {self.point.y})"




class maplocation(models.Model):
    location = models.PointField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"maplocation({self.location.x}, {self.location.y})"
