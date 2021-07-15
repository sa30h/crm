from .models import *
from rest_framework import serializers

class ServiceSerializer(serializers.ModelSerializer):
    model   = Service
    fields  = '__all__'

