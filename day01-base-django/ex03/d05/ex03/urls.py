from . import views
from django.urls import path


urlpatterns = [path("", views.table_shades, name="table_shades")]
