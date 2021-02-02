from django.urls import path

from . import views

urlpatterns = [
    path('', views.instructions, name='instructions'),
    path('<int:respondent_id>/<int:position>/', views.driver, name='driver'),
    path('survey<int:respondent_id>/<int:position>/', views.survey, name='survey'),
    path('thoughts<int:respondent_id>/<int:position>/', views.thoughts, name='thoughts'),
    path('thanks<int:respondent_id>/<int:position>/', views.thanks, name='thanks'),
    path('export_ratings/', views.export_ratings, name='ratings'),
    path('export_users/', views.export_users, name='users'),
    path('export_products/', views.export_products, name='products'),
]