
from django.forms import ValidationError
from django.utils                   import timezone
from django.contrib                 import admin
from django.db.models               import F
from django.utils.html              import format_html
import json
from django.utils.safestring        import mark_safe
from django.db.models import Sum
from django.utils.html import format_html, mark_safe
from django.contrib import admin
import json

from api_logs.models import APILog
class APILogAdmin(admin.ModelAdmin):
    list_display        = ('method', 'path', 'formatted_response_status','formatted_user', 'ip_address',  'timestamp')
    list_filter         = ('method', 'response_status', 'user')
    search_fields       = ('method', 'path', 'ip_address')
    readonly_fields     = ('method', 'path', 'formatted_request_body', 'formatted_response_body', 'response_status', 'error_message', 'duration', 'timestamp', 'user', 'ip_address', 'headers', 'query_params', 'user_agent','timestamp', 'formatted_duration', )
    exclude             = ('request_body', 'response_body')

    def formatted_response_status(self, obj):
        if 200 <= obj.response_status < 300:
            color = 'green'  # Success codes
        elif 300 <= obj.response_status < 400:
            color = 'goldenrod'  # Redirection codes
        elif 400 <= obj.response_status < 500:
            color = 'red'  # Client errors
        elif 500 <= obj.response_status:
            color = 'darkred'  # Server errors
        return format_html('<span style="color: {};">{}</span>', color, obj.response_status)

    def formatted_duration(self, obj):
        duration_seconds = obj.duration / 1000.0
        return format_html('{}s', round(duration_seconds, 2))

    def formatted_user(self, obj):
        return format_html('<span style="color: #333399;">{}</span>', obj.user.email if obj.user else "Anonymous")

    def formatted_request_body(self, obj):
        try:
            json_data = json.loads(obj.request_body)
            pretty_json = json.dumps(json_data, indent=4)
            return mark_safe(f'<pre style="background-color: #333; color: #f5f5f5; padding: 10px; border-radius: 5px; border: 1px solid #444;">{pretty_json}</pre>')
        except json.JSONDecodeError:
            return mark_safe(f'<pre style="background-color: #333; color: #f5f5f5;">{obj.request_body}</pre>')

    def formatted_response_body(self, obj):
        try:
            json_data = json.loads(obj.response_body)
            pretty_json = json.dumps(json_data, indent=4)
            return mark_safe(f'<pre style="background-color: #333; color: #f5f5f5; padding: 10px; border-radius: 5px; border: 1px solid #444;">{pretty_json}</pre>')
        except json.JSONDecodeError:
            return mark_safe(f'<pre style="background-color: #333; color: #f5f5f5;">{obj.response_body}</pre>')


    formatted_request_body.short_description        = 'Request Body'
    formatted_response_body.short_description       = 'Response Body'
    formatted_user.short_description                = 'User'
    formatted_duration.short_description            = 'Duration'
    formatted_response_status.short_description     = 'Response Status'
    
admin.site.register(APILog, APILogAdmin)