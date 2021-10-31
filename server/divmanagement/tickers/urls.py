from django.urls import path
from tickers import views

urlpatterns = [
    path('tickers/', views.ticker_list),
    path('tickers/<int:pk>/', views.ticker_detail),
]
