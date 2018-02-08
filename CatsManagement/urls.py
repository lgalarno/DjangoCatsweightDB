from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'CatsManagement'

urlpatterns = [
    path('create-cat/', login_required(views.CreateCatView.as_view()), name = "CreateCatView"),
    path('delete-cat/<int:id>/<slug>/', login_required(views.CatDeleteView.as_view()), name = "CatDeleteView"),
    path('cat/<int:id>/<slug>/change/', login_required(views.CatUpdateView.as_view()), name = "CatUpdateView"),
    path('<int:id>/<slug>/', views.CatDetailView.as_view(), name = "CatDetailView"),
    path('', views.CatsListView.as_view(), name = "CatsListView"),
]

