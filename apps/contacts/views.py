from rest_framework import viewsets
from .models import Contact, ContactPoint
from .serializers import ContactSerializer, ContactPointSerializer


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        qs = Contact.objects.filter(
            company=self.request.company
        ).prefetch_related('contact_points').order_by('name')
        is_vendor   = self.request.query_params.get('is_vendor')
        is_customer = self.request.query_params.get('is_customer')
        if is_vendor   == 'true': qs = qs.filter(is_vendor=True)
        if is_customer == 'true': qs = qs.filter(is_customer=True)
        return qs

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            company=self.request.company,
        )


class ContactPointViewSet(viewsets.ModelViewSet):
    serializer_class = ContactPointSerializer

    def get_queryset(self):
        return ContactPoint.objects.filter(
            contact__company=self.request.company
        ).select_related('contact')

    def perform_create(self, serializer):
        serializer.save()
