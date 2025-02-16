from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from .views import ReferenceBookListView, ReferenceBookElementsView, CheckElementView
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('refbooks/', ReferenceBookListView.as_view(), name='refbooks'),
    path("refbooks/<int:refbook_id>/elements/", ReferenceBookElementsView.as_view(), name="refbook-elements"),
    path('refbooks/<int:id>/check_element', CheckElementView.as_view(), name='check_element'),

]