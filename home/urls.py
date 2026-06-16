from django.contrib import admin
from django.urls import path
from .views import home, contact_submit
from .views import add_player, remove_player, update_player, player_detail
import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    # Player URLs
    path('players/add/', add_player, name='add_player'),
    path('players/<uuid:player_id>/remove/', remove_player, name='remove_player'),
    path('players/<uuid:player_id>/update/', update_player, name='update_player'),
    path('players/<uuid:player_id>/', player_detail, name='player_detail'), 
]
