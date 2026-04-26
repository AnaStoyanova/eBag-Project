import django_filters
from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    sku = django_filters.CharFilter(lookup_expr='iexact')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    # Matches the given category AND all its descendants
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(), method='filter_category'
    )

    class Meta:
        model = Product
        fields = ['title', 'sku', 'price_min', 'price_max', 'category']

    def filter_category(self, queryset, name, value):
        descendants = value.get_descendants(include_self=True)
        return queryset.filter(category__in=descendants)
