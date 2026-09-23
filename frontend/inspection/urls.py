"""
URLs para la aplicación de inspección vehicular
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="root_login"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("inspect/", views.inspect_view, name="inspect"),
    path("report/", views.report_view, name="report"),
]
