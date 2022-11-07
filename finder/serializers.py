from rest_framework import serializers
from finder.models import FinderModel


class FinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinderModel
        fields = '__all__'
