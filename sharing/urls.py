from django.urls import path
from . import views

app_name = 'sharing'

urlpatterns = [
    path('', views.index, name='index'),
    path('share/done/<str:token>/', views.share_done, name='share_done'),
    path('share/<str:token>/claim/', views.claim_view, name='claim'),
    path('download/<str:token>/', views.download_view, name='download'),
    path('share/<str:token>/decline/', views.decline_view, name='decline'),
]
