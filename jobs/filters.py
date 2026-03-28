# jobs/filters.py
import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):


    job_type = django_filters.BaseInFilter(
        field_name='job_type',
        lookup_expr='in'
    )
    experience = django_filters.ChoiceFilter(
        field_name='experience',
        choices=[
            ('junior',  'Junior'),
            ('mid',     'Mid'),
            ('senior',  'Senior'),
        ]
    )
    location      = django_filters.CharFilter(field_name='location',     lookup_expr='icontains')
    title         = django_filters.CharFilter(field_name='title',        lookup_expr='icontains')
    company       = django_filters.CharFilter(field_name='company',      lookup_expr='icontains')

    # salary range
    min_salary    = django_filters.NumberFilter(field_name='salary',     lookup_expr='gte')
    max_salary    = django_filters.NumberFilter(field_name='salary',     lookup_expr='lte')

    # date range
    posted_after  = django_filters.DateFilter(field_name='created_at',  lookup_expr='gte')
    posted_before = django_filters.DateFilter(field_name='created_at',  lookup_expr='lte')

    # boolean
    is_active     = django_filters.BooleanFilter(field_name='is_active')

    # multiple values  e.g. ?skills=python&skills=django
    skills        = django_filters.CharFilter(field_name='skills__name', lookup_expr='icontains')

    class Meta:
        model  = Job
        fields = [
            'job_type', 'location', 'title',
            'company',  'is_active', 'skills',
        ]