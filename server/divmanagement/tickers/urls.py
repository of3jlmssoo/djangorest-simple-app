from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from tickers import views

# API endpoints
urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('tickers/',
         views.TickerList.as_view(),
         name='ticker-list'),
    path('tickers/<int:pk>/',
         views.TickerDetail.as_view(),
         name='ticker-detail'),
    # path('snippets/<int:pk>/highlight/',
    #     views.SnippetHighlight.as_view(),
    #     name='snippet-highlight'),
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


# from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns

# from tickers import views

# urlpatterns = [
#     # path('tickers/', views.ticker_list),
#     # path('tickers/<int:pk>/', views.ticker_detail),
#     path('tickers/', views.TickerList.as_view()),
#     path('tickers/<int:pk>/', views.TickerDetail.as_view()),
#     path('', views.api_root),


# ]
# urlpatterns = format_suffix_patterns(urlpatterns)
