from django.urls import include, path

from .views import HomePageView, api


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('api', api, name='api'),
]
