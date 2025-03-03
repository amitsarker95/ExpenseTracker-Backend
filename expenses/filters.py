from django_filters.rest_framework import DjangoFilterBackend

class BudgetFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category_name = request.query_params.get('category', None) 
        if category_name:
            queryset = queryset.filter(category__name=category_name)  
        return queryset
