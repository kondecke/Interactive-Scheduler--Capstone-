from rest_framework import serializers
from . import models
class eventSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = models.Event 
        fields = ['eventid', 'time', 'description', 'alert', 'accesslevel']

class loginSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = models.Logins
        fields = ['studentid', 'pwd']

