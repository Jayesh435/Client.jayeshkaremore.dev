from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('<int:project_id>/', views.payment_detail, name='payment_detail'),
]
