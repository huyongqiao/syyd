import logging

from django.utils.deprecation import MiddlewareMixin


record_ip_logger = logging.getLogger('record_ip')

class RecordIP(MiddlewareMixin):
    def __call__(self, request):
        ip = request.META['REMOTE_ADDR']
        path = request.path
        record_ip_logger.info('%s %s' % (ip, path))
        response = self.get_response(request)
        return response
