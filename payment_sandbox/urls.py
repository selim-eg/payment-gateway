"""
URL configuration for payment_sandbox project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.views.static import serve

from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
       openapi.Info(
           title="API Documentation",
           default_version='v1',
           description="""API documentation for my project
               

                        These cards can be used to test payment transactions in the application.

                        | Name           | NUMBER            | CVC         | DATE            | Status
                        |-----------------|-------------------|-------------|-----------------|-------
                        | mohamed selim   | 4242424242424242  | 123         | 01 / 25         | success
                        | omar ahmed      | 4000056655665556  | 456         | 02 / 26         | cancel
                        | khaled said     | 4343434343434343  | 789         | 03 / 27         | failure
                        
                        """,
           terms_of_service="https://www.google.com/policies/terms/",
           contact=openapi.Contact(email="contact@myproject.local"),
           license=openapi.License(name="BSD License"),
       ),
       public=True,
       permission_classes=(permissions.AllowAny,),
   )


urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,
    {'document_root': settings.MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
 
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('transactions/', include('transactions.urls', namespace='transactions')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('webhooks/', include('webhooks.urls', namespace='webhooks')),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]
