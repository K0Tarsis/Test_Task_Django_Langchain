from rest_framework.pagination import PageNumberPagination


class ThreeItemPagination(PageNumberPagination):
    page_size = 3