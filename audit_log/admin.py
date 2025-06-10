from django.contrib import admin
from rest_framework_tracking.models import APIRequestLog

@admin.register(APIRequestLog)
class APIRequestLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'requested_at', 'path', 'method', 'status_code', 'remote_addr')
    search_fields = ('user__username', 'path')
    list_filter = ('method', 'status_code', 'requested_at')
