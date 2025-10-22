from django.urls import path
from .views import SetLanguageView

urlpatterns = [
    path('set-language/<str:language_code>/', SetLanguageView.as_view(), name='set_language'),
]
