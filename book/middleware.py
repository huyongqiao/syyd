import logging

from django.utils.deprecation import MiddlewareMixin


record_ip_logger = logging.getLogger('record_ip')

# 在线下request.META['REMOTE_ADDR']可以获取真实IP
# 在线上部署后，用户IP都被nginx拦截了，传入django的IP都是127.0.0.1
# 使用nginx后，使用request.META['HTTP_X_FORWARDED_FOR']获取真实IP
class RecordIP(MiddlewareMixin):
    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            pass
        else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.
            # Take just the first one.
            real_ip = real_ip.split(",")[0]
            request.META['REMOTE_ADDR'] = real_ip

        ip = request.META['REMOTE_ADDR']
        path = request.path
        record_ip_logger.info('%s %s' % (ip, path))
