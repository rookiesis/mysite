from django.urls import path

from .views import base_views, lecture_views

app_name = "lecture"

urlpatterns = [
    # base_views.py
    path('', base_views.index, name='index'), # 127.0.0.1:8000/lecture/
    path('<int:lecture_id>/', base_views.detail, name='detail'),
    # lecture_views.py
    path('lecture/create/', lecture_views.lecture_create, name="lecture_create"),
    path('lecture/modify/<int:lecture_id>/', lecture_views.lecture_modify, name='lecture_modify'),
    path('lecture/delete/<int:lecture_id>/', lecture_views.lecture_delete, name="lecture_delete"),
]