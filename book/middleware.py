import logging

from django.utils.deprecation import MiddlewareMixin


record_ip_logger = logging.getLogger('record_ip')

# 在线下生效，在线上部署后，用户IP都被nginx拦截了，传入django的IP都是127.0.0.1
class RecordIP(MiddlewareMixin):
    def __call__(self, request):
        ip = request.META['REMOTE_ADDR']
        path = request.path
        record_ip_logger.info('%s %s' % (ip, path))
        response = self.get_response(request)
        return response
