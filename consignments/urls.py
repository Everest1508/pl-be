from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, ConsignmentViewSet, CustomEmailLoginView

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'consignments', ConsignmentViewSet, basename='consignment')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', CustomEmailLoginView.as_view(), name='custom-login'),
]
