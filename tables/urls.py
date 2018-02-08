from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from . import views

app_name = 'tables'

urlpatterns = [
    #path('', views.webtables, name="webtables"),
    path('', views.WebtablesView.as_view(), name="WebtablesView"),
    path('csv', views.csvweb, name="csvweb"),
    path('select', views.SelectView.as_view(), name="SelectView"),
    path('chart', views.ChartView.as_view(), name="ChartView"),
]
