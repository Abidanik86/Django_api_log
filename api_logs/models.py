# api_logging/models.py
from django.db                  import models
from django.conf                import settings
from core.settings              import AUTH_USER_MODEL
from django.utils               import timezone
class APILog(models.Model):
    method              = models.CharField(max_length=10)
    path                = models.CharField(max_length=200)
    request_body        = models.JSONField()
    response_status     = models.IntegerField()
    response_body       = models.JSONField()
    error_message       = models.TextField(null=True, blank=True)
    duration            = models.FloatField()
    timestamp           = models.DateTimeField(default=timezone.now)
    user                = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address          = models.GenericIPAddressField(null=True, blank=True)
    headers             = models.JSONField(null=True, blank=True)
    query_params        = models.JSONField(null=True, blank=True)
    user_agent          = models.CharField(max_length=255, null=True, blank=True)
    ip_address          = models.CharField(max_length=50 , null=True, blank=True)
    def __str__(self):
        return f"{self.method} {self.path} - {self.response_status}"
