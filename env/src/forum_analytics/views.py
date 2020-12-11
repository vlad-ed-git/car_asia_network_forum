from django.shortcuts import render
from .models import ForumAnalytics, LogKey, LogType

# Create your views here.
def get_analytics_count(log_key, user=None):
    total_found = ForumAnalytics.objects.filter(log_key=log_key,user=user).count()
    return total_found


def saveAnalytics(log_key, log_value, log_type, resolved, request = None, user=None):
    try:
        ip_address = None
        if request:
            ip_address = get_client_ip(request)
        analytics  = ForumAnalytics(log_key=log_key, log_value=log_value, log_type=log_type, resolved=resolved, ip_address=ip_address, user=user)
        analytics.save()
    except Exception as err:
       print(err)


def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except Exception as err:
        print("-------------------------Getting IP Address Err")
        print(str(err))
        print("---------------- END EXCEPTION MSG ---------")
        return None



