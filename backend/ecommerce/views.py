from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import ItemSerializer, OrderSerializer
from .models import Item, Order
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin


class ItemViewSet(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """A simple ViewSet for listing or retrieving items."""
    permission_classes = (IsAuthenticated,)  # permission to show items only to users with received token
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrderViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    """A simple ViewSet for listing, retrieving and creating orders."""
    permission_classes = (IsAuthenticated,)  # permission to show orders only to users with received token
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        This view should return a list of all the orders
        for the currently authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(user=user)

    def create(self, request):
        """Order Creation Method"""
        try:
            data = JSONParser().parse(request)  # extract the completed order data
            serializer = OrderSerializer(data=data)  # passing data to serializer
            # if there is enough stock, we do not create an order directly, but call the place_order method
            # And after that we transfer it to the sterilizer of the Order
            if serializer.is_valid(raise_exception=True):
                item = Item.objects.get(pk=data["item"])
                order = item.place_order(request.user, data["quantity"])
                return Response(OrderSerializer(order).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)
