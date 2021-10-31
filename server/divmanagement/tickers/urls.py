from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from tickers import views

urlpatterns = [
    # path('tickers/', views.ticker_list),
    # path('tickers/<int:pk>/', views.ticker_detail),
    path('tickers/', views.TickerList.as_view()),
    path('tickers/<int:pk>/', views.TickerDetail.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
