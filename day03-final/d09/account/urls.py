from django.urls import path
from account.views import AccountView, LogoutView


urlpatterns = [
    path('account/', AccountView.as_view(), name='account'),
    path('account/logout/', LogoutView.as_view(), name='logout'),
]