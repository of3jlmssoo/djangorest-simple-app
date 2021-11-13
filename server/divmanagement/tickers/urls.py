from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from tickers import views

# API endpoints
urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    #     re_path(r'^tickersname/(?P<ticker>\w+)/$', views.TickerListAPIView.as_view()),
    path('tickersname/', views.TickerListAPIView.as_view()),
    path('tickers/',
         views.TickerList.as_view(),
         name='ticker-list'),
    path('tickers/<int:pk>/',
         views.TickerDetail.as_view(),
         name='ticker-detail'),

    path('users/',
         views.UserList.as_view(),
         name='user-list'),
    path('users/<int:pk>/',
         views.UserDetail.as_view(),
         name='user-detail'),

    path('dividends/',
         views.DividendList.as_view(),
         name='dividend-list'),
    path('dividends/<int:pk>/',
         views.DividendDetail.as_view(),
         name='dividend-detail'),
])
