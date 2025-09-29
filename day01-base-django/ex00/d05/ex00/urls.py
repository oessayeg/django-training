from . import views
from django.urls import path


urlpatterns = [path("", views.markdown_info_view)]
