from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from home.views import home, contact_submit, robots_txt, add_player, remove_player, update_player, player_detail
from home.sitemaps import StaticViewSitemap, BlogPostSitemap
from django.conf.urls.static import static

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogPostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('contact/', contact_submit, name='contact_submit'),
    path('players/add/', add_player, name='add_player'),
    path('players/<uuid:player_id>/remove/', remove_player, name='remove_player'),
    path('players/<uuid:player_id>/update/', update_player, name='update_player'),
    path('players/<uuid:player_id>/', player_detail, name='player_detail'),
    path('summernote/', include('django_summernote.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)