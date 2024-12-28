import json
import time
from django.utils.deprecation import MiddlewareMixin
from .models import APILog

class APILoggingMiddleware(MiddlewareMixin):
    MASKED_FIELDS = ['password', 'refresh', 'access', 'Authorization']  

    def process_request(self, request):
        request.api_start_time      = time.time()
        request.user_ip             = self.get_client_ip(request)
        request.api_headers         = dict(request.headers)
        self.mask_sensitive_fields(request.api_headers, is_header=True)
        request.api_query_params    = dict(request.GET)
        request.api_user_agent      = request.META.get('HTTP_USER_AGENT', '')  
        request.api_body            = self.get_request_body(request)

    def process_response(self, request, response):
        try:
            if self.should_log(request.path):
                duration = time.time() - request.api_start_time
                response_body = self.get_response_body(response)

                APILog.objects.create(
                    method              = request.method,
                    path                = request.get_full_path(),
                    request_body        = request.api_body if request.api_body is not None else '',
                    response_status     = response.status_code,
                    response_body       = response_body if response_body is not None else '',
                    duration            = duration,
                    user                = request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
                    ip_address          = request.user_ip,
                    headers             = request.api_headers,
                    query_params        = request.api_query_params,
                    user_agent          = request.api_user_agent 
                )
        except Exception as e:          
            print("Error while logging API request:", e)

        return response

    def process_exception(self, request, exception):
        try:
            if self.should_log(request.path):
                duration = time.time() - request.api_start_time
                
                APILog.objects.create(
                    method          = request.method,
                    path            = request.get_full_path(),
                    request_body    = request.api_body if request.api_body is not None else '',
                    response_status = 500,
                    response_body   = '',
                    error_message   = str(exception),
                    duration        = duration,
                    user            = request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
                    ip_address      = request.user_ip,
                    headers         = request.api_headers,
                    query_params    = request.api_query_params,
                    user_agent      = request.api_user_agent
                )
        except Exception as e:
            print("Error while logging API exception:", e)

    def should_log(self, path):
        # Add Your Main App Core where the settings.py from there add the urls.py path's 
        # Example("your app path")
        return path.startswith("/api/users/") or path.startswith("/api/fcc/")   

    def get_request_body(self, request):
        try:
            if request.content_type == 'application/json':
                request_data = json.loads(request.body.decode('utf-8')) if request.body else None
                if request_data:
                    self.mask_sensitive_fields(request_data)
                return json.dumps(request_data) if request_data else ''
            elif request.content_type == 'application/x-www-form-urlencoded':
                request_data = request.POST.dict() if request.POST else None
                if request_data:
                    self.mask_sensitive_fields(request_data)
                return json.dumps(request_data) if request_data else ''
            elif request.content_type == 'multipart/form-data':
                request_data = {k: v if isinstance(v, str) else str(v) for k, v in request.POST.items()} if request.POST else None
                if request_data:
                    self.mask_sensitive_fields(request_data)
                return json.dumps(request_data) if request_data else ''
            else:
                return ''
        except Exception as e:
            print("Error while parsing request body:", e)
            return ''

    def get_response_body(self, response):
        try:
            response_data = json.loads(response.content.decode('utf-8')) if response.content else None
            if response_data:
                self.mask_sensitive_fields(response_data)
            return json.dumps(response_data) if response_data else ''
        except Exception as e:
            print("Error while parsing response body:", e)
            return ''

    def mask_sensitive_fields(self, data, is_header=False):
        for field in self.MASKED_FIELDS:
            if isinstance(data, dict):
                if field in data:
                    if is_header and field == 'Authorization':
                        data[field] = '***'  # Mask entire Authorization header
                    else:
                        data[field] = self.mask_token_field(data[field])
                for key, value in data.items():
                    if isinstance(value, dict) or isinstance(value, list):
                        self.mask_sensitive_fields(value)
            elif isinstance(data, list):
                for item in data:
                    self.mask_sensitive_fields(item)

    def mask_token_field(self, value):
        if isinstance(value, str):
            if len(value) > 10:
                return value[:5] + '*' * 5
            else:
                return '*' * len(value)
        return '*' * len(str(value))

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
