from rest_framework import serializers
from models import * 
class eventSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Event 
        fields = ['eventid', 'time', 'description', 'alert', 'accesslevel']

