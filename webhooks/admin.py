from django.contrib import admin
from .models import WebhookEndpoint, WebhookEvent

@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'url', 'is_test', 'secret', 'status', 'created_at', 'updated_at')
    list_filter = ('is_test', 'status', 'created_at')
    search_fields = ('description', 'url', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'description', 'url', 'is_test')
        }),
        ('Security', {
            'fields': ('secret',),
            'classes': ('collapse',),
        }),
        ('Status', {
            'fields': ('status',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'event_type', 'date_occurred', 'date_sent', 'status', 'attempt_count', 'response_status')
    list_filter = ('status', 'date_occurred', 'date_sent')
    search_fields = ('event_type', 'endpoint__description', 'response_status')
    readonly_fields = ('created_at', 'updated_at', 'date_occurred', 'date_sent')

    fieldsets = (
        (None, {
            'fields': ('endpoint', 'event_type', 'data')
        }),
        ('Delivery Status', {
            'fields': ('status', 'attempt_count', 'response_status', 'response_body'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('date_occurred', 'date_sent', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request, obj=None):
        
        return False

    def has_delete_permission(self, request, obj=None):
        
        return True
