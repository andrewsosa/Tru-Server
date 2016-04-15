from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

from CodeCamp.models import School
from CodeCamp.serializer import SchoolSerializer

import django_filters


class SchoolFilter(filters.FilterSet):
    min_IS = django_filters.NumberFilter(name="tuitionIS", lookup_type='gte')
    max_IS = django_filters.NumberFilter(name="tuitionIS", lookup_type='lte')
    class Meta:
        model = School
        fields = [
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
        ]

# Create your views here.
class SchoolViewSet(viewsets.ModelViewSet):
    """
    API endpoint for schools.
    """

    serializer_class = SchoolSerializer
    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SchoolFilter
    queryset = School.objects.all()
