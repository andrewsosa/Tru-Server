from rest_framework import serializers
from CodeCamp.models import School

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = (
            'id',
            'name',
            'tuitionIS',
            'tuitionOS',
            'enrollGrad',
            'enrollUnder',
            'budget',
            'endowment',
            'researchExp',
            'datasource',
            'ranking'
        )
