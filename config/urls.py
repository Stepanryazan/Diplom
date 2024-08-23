from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
       openapi.Info(
           title="My API",
           default_version='v1',
           description="Documentation for My API",
           terms_of_service="http://localhost:8000",
           contact=openapi.Contact(email="contact@example.com"),
           license=openapi.License(name="BSD License"),
       ),
       public=True,
       permission_classes=(permissions.AllowAny,),
   )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='user')),
    path('app/', include('app.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs.json/', schema_view.without_ui(), name='schema-json'),
]
