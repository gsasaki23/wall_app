from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index),
    path('success', views.success),
    path('attempt_login', views.attempt_login),
    path('attempt_reg', views.attempt_reg),
    path('attempt_message', views.attempt_message),
    path('attempt_comment', views.attempt_comment),
    path('attempt_delete', views.attempt_delete),
    path('logout', views.logout),
]