from os import name
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Pastebin API')
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)



urlpatterns = [
    path('swagger/', schema_view),
    path('', include(router.urls)),
    path('auth/',obtain_auth_token),
    path('profile/',views.profile, name='profile'),
    path('content/',views.content, name='content'),





    

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)






