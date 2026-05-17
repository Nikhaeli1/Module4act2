from django.contrib import admin
from django.urls import path
from payments.views import UserRegistrationView, SecurePaymentView # Make sure both are imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/payments/', SecurePaymentView.as_view(), name='payments'), # Add this line!
]