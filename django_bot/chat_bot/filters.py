from django_filters import rest_framework as filters

from chat_bot.models import Homes


class HomesFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_area = filters.NumberFilter(field_name="area", lookup_expr='gte')
    max_area = filters.NumberFilter(field_name="area", lookup_expr='lte')
    min_bedrooms = filters.NumberFilter(field_name="bedrooms", lookup_expr='gte')
    max_bedrooms = filters.NumberFilter(field_name="bedrooms", lookup_expr='lte')
    min_bathrooms = filters.NumberFilter(field_name="bathrooms", lookup_expr='gte')
    max_bathrooms = filters.NumberFilter(field_name="bathrooms", lookup_expr='lte')

    bathrooms = filters.NumberFilter(field_name="bathrooms")
    bedrooms = filters.NumberFilter(field_name="bedrooms")
    address = filters.CharFilter(field_name="address", lookup_expr='icontains')
    type_of_purchase = filters.ChoiceFilter(field_name="type_of_purchase", choices=list(Homes.TYPE_OF_PURCHASE.items()))

    class Meta:
        model = Homes
        fields = [
            'min_price', 'max_price',
            'min_area', 'max_area',
            'min_bedrooms', 'max_bedrooms',
            'min_bathrooms', 'max_bathrooms',
            'bathrooms', 'bedrooms',
            'address', 'type_of_purchase'
        ]