from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins, permissions

from .filters import ReserveFilter
from .models import Reserve

from .serializers import ReserveSerializer

class ReserveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Reserve.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReserveSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ReserveFilter

    def get_queryset(self):
        user = self.request.user
        return Reserve.objects.filter(user=user)




