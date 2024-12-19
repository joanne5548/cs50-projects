from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/results", views.results_view, name="results"),
    path("wiki/create", views.create_view, name="create"),
    path("wiki/<str:entry_name>", views.entry_view, name="entry"),
]
