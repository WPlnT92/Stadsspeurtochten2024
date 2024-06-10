from django.urls import path

from . import views

app_name = "speurtochten"
urlpatterns = [
    path("", views.index, name="index"),
    path('over/', views.over, name='over'),
    path('contact/', views.contact, name='contact'),
    path('overzicht/', views.overzicht, name='overzicht'),
    path('speurtocht/<str:name>/', views.speurtocht, name='speurtocht'),
    path('speurtocht/<str:name>/bestellen/', views.bestellen, name='bestellen'),
    path('speurtocht/<str:name>/verdergaan/', views.verdergaan, name='verdergaan'),
    path('speurtocht/<str:name>/begin/<str:gt_code>/', views.begin, name='begin'),
    path('speurtocht/<str:name>/<str:gt_code>/question/<int:num>/<int:pk>/map/', views.map, name='map'),
    path('speurtocht/<str:name>/<str:gt_code>/question/<int:num>/<int:pk>/', views.question, name='question'),
    path('speurtocht/<str:name>/<str:gt_code>/answer/<int:num>/<int:pk>/', views.answer, name='answer'),
    path('speurtocht/<str:name>/<str:gt_code>/finished/', views.finish, name='finish'),
    path('algemene-voorwaarden/', views.algemenevoorwaarden, name='algemenevoorwaarden')
]
