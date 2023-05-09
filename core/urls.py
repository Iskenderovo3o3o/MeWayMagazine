from django.contrib import admin
from django.urls import path,include

import users
from core.yasg import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/posts/', include('posts.urls')),
    path('api/v1/users/', include('users.urls')),
]


