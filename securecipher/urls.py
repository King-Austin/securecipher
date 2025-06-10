"""
URL configuration for securecipher project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include

# What it does: Customizes the default Django admin interface branding
admin.site.site_header = 'SecureCipher Administration'
admin.site.site_title = 'SecureCipher Admin'
admin.site.index_title = 'Welcome to SecureCipher Admin Portal'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),  # User management endpoints
    #path('api/crypto/', include('crypto_engine.urls')),  # Cryptography endpoints
    #path('api/transactions/', include('transactions.urls')),  # Transaction endpoints
    #path('api/audit/', include('audit_log.urls')),  # Audit log endpoints
    #path('api/tls/', include('tls_middleware.urls')),  # TLS middleware endpoints
]
