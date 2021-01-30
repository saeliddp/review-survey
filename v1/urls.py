from django.urls import path

from . import views

urlpatterns = [
    path('', views.entry, name='entry'),
    path('<int:respondent_id>/<int:position>/', views.driver, name='driver'),
    path('instructions<int:respondent_id>/<int:position>/', views.instructions, name='instructions'),
    path('survey<int:respondent_id>/<int:position>/', views.survey, name='survey'),
    path('thanks<int:respondent_id>/', views.thanks, name='thanks'),
    path('export_ratings/', views.export_ratings, name='ratings'),
    path('export_users/', views.export_users, name='users'),
    path('export_products/', views.export_products, name='products'),
]