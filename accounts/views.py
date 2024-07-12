from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import HttpResponse



class AccountsViewSet(ViewSet):

    def list(self, request):
        return Response({'message': 'All accounts'})
    


