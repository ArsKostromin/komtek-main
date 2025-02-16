from rest_framework import serializers
from .models import ReferenceBook, ReferenceBookVersion, ReferenceBookElement


class ReferenceBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceBook
        fields = ("id", "code", "name")
        

class ReferenceBookElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceBookElement
        fields = ("code", "value")
