from django.urls import path
from users import views


urlpatterns = [
    path('registration/', views.RegisterApiView.as_view()),
    path('authorization/', views.AuthorizationApiView.as_view()),
    path('confirm/', views.ConfirmationApiView.as_view()),
]
