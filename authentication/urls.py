from django.urls import path
from .views import LoginView, RegisterView, VerificationView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify/', VerificationView.as_view()),
    path('login/', LoginView.as_view()),
]