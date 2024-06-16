import django_filters
from django import forms
from .models import Peladas_bd

class PeladasFilter(django_filters.FilterSet):
    class Meta:
        model = Peladas_bd
        fields = {
            "preço": ["exact"],
            "dia": ["exact"],
            "hora": ["exact"],
            "nota": ['gt'],
            "nome": ["icontains"],
        }
