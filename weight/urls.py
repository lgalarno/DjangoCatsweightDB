from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'weight'

urlpatterns = [
    path('measure/',login_required(views.EnterWeight), name = "EnterWeight"),
    path('confirm/', login_required(views.WeightConfirm), name = "WeightConfirm"),
    path('save/', login_required(views.SaveWeight), name = "SaveWeight")
]
