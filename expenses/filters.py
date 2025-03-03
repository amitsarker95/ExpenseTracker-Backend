from django_filters.rest_framework import DjangoFilterBackend

class BudgetFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)