from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("terms/", views.term_list, name="term_list"),
    path("terms/<slug:slug>/", views.term_detail, name="term_detail"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),
    path("about/", views.about_project, name="about"),
    path("suggest/", views.submit_suggestion, name="submit_suggestion"),
]
