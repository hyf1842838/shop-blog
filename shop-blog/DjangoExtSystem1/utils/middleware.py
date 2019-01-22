
import logging
import time

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from users.models import User


class TestMiddlware(MiddlewareMixin):

    def process_request(self, request):
        print('请求request')
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('process_view')

    def process_template_response(self, request, response):
        # 默认不执行，只有当视图函数返回render的时候，才会被调用
        print('process_template_response')
        return response

    def process_exception(self, request, exception):
        # 默认不执行，只有当视图函数出现bug的时候，才会被调用
        print('process_except')
        # process_exception 方法有了返回值就不再执行其他中间件的process_exception，直接执行response方法响应
        return HttpResponse('出错啦')
    #
    def process_response(self, request, response):
        print('响应response')
        # 响应一定要加return response
        return response


class TestMiddlware1(MiddlewareMixin):

    def process_request(self, request):
        print('test1 process_request')

    def process_response(self, request, response):
        print('test1 process_response')
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('test1 process_view')

    def process_exception(self, request, exception):
        print('test1 process_except')

    def process_template_response(self, request, response):
        print('test1 process_template_response')
        return response

class TestMiddlware2(MiddlewareMixin):

    def process_request(self, request):
        print('test2 process_request')

    def process_response(self, request, response):
        print('test2 process_response')
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('test2 process_view')

    def process_exception(self, request, exception):
        print('test2 process_except')

    def process_template_response(self, request, response):
        print('test2 process_template_response')
        return response

# 获取logger
logger = logging.getLogger(__name__)

class LogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # url到服务器的时候，经过中间件最先执行的方法
        request.init_time = time.time()
        request.init_body = request.body

    def process_response(self, request, response):
        try:
            # 经过中间件，最后执行的方法
            # 计算请求到响应的时间
            count_time = time.time() - request.init_time
            # 获取响应的状态码
            code = response.status_code
            # 获取请求的内容
            req_body = request.init_body
            # 获取想要的内容
            res_body = response.content

            msg = '%s %s %s %s' % (count_time, code, req_body, res_body)
            # 写入日志信息
            logger.info(msg)
        except Exception as e:
            logger.critical('log error, Exception:%s' % e)

        return response


class UserAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            # 获取登录时, 向request.session中保存的user_id值
            user_id = request.session['user_id']
            user = User.objects.filter(pk=user_id).first()
            request.user = user
        except:
            # 如果不能从request.session中获取到user_id键值对，则跳转到登录
            return HttpResponseRedirect(reverse('users:login'))

        return None

