from django_filters import rest_framework as filters

from reserve.models import Reserve


class ReserveFilter(filters.FilterSet):
    total_sum_from = filters.NumberFilter(field_name='total_sum',
                                          lookup_expr='gte')
    total_sum_to = filters.NumberFilter(field_name='total_sum',
                                        lookup_expr='lte')
    created_at = filters.DateFilter(field_name='created')
    created_at = filters.DateTimeFromToRangeFilter()


    class Meta:
        model = Reserve
        fields = ('status',)
