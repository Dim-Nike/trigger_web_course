from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('', show_home, name='home'),
    path('register/', show_register, name='register'),
    path('login/', show_login, name='login'),
    path('item/<int:pk>', show_item, name='item'),
    path('author/', show_author, name='author'),
    path('collection/', show_collection, name='collection'),
    path('create/', show_create, name='create'),
    path('index/', show_index, name='index'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)