import re

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from goods.models import Goods
from user.models import User
from utils.forms import SearchForm

# 检测登陆状态
class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 拦截请求之前的函数
        # try:

            # 搜索
            if request.method == 'POST':
                path = request.path
                not_path = ['/cart/cart/', '/goods/index/', '/goods/detail/.*/', '/goods/list_goods/.*/', '/order/place_order/',
                            '/order/user_order/', '/user/user_center_site/', '/user/user_info/']
                for ch_path in not_path:
                    if re.match(ch_path, path):
                        form = SearchForm(request.POST)
                        if form.is_valid():
                            name = form.cleaned_data['searchgoods']
                            goods = Goods.objects.filter(name__contains=name).first()
                            return render(request, 'detail.html', {'good': goods})
                        else:
                            return HttpResponseRedirect(reverse('goods:index'))


            # 判断是否处于登陆状态
            # 1.给request.user属性赋值，赋值为当前登陆系统的用户
            user_id = request.session.get('user_id')
            if user_id:
                # 拿到用户对象
                user = User.objects.filter(pk=user_id).first()
                # 请求中的用户属性改为当前登陆用户对象
                request.user = user
            # 2 .登陆校验，需区分哪些地址需要做登陆校验，哪些地址不需要做登陆校验
            path = request.path
            if path == '/':
                # 如果直接访问不带路由的地址(通常为主页)，则不用进行强制登陆(也可在下面不用校验的集合中写成
                # '^/$‘，则此处不用写这个if语句)。
                return None
            # 不需要做登陆校验的地址
            not_need_check = ['/user/register/', '/user/login/', '/goods/index/',
                              '/goods/detail/.*/', '/cart/.*/','/user/user_info/']

            # 历史记录
            if user_id:
                if re.match('/goods/detail/.*/', path):
                    history = request.session.get('history', [])
                    for his in history:
                        if int(path[14:-1]) == his:
                            history.remove(his)
                            break
                    history.insert(0, int(path[14:-1]))
                    request.session['history'] = history

            for check_path in not_need_check:
                if re.match(check_path, path):
                    # 当前path路径为不需要做登陆校验的路由，则直接访问对应页面
                    return None
            if not user_id:
                # path为需要做登陆校验的路由时，判断用户是否登陆，没有登陆则跳转到登陆页面
                return HttpResponseRedirect(reverse('user:login'))




        # except Exception as e:
        #     return HttpResponseRedirect(reverse('goods:index'))


class SessionToMiddleware(MiddlewareMixin):
    # 同步数据库与session中的数据
    def process_response(self, request, response):
        # 同步session中的商品信息和数据库中购物车表的商品信息
        #1.判断用户是否登陆，登陆才做数据同步操作
        user_id = request.session.get('user_id')
        if user_id:
            # 2.同步
            # 2.1判断session中的商品是否存在于数据库中，如果存在，则更新
            # 2.2如果不存在，则创建
            # 2.3同步数据库的数据到session中
            session_goods = request.session.get('goods')
            if session_goods:
                # 将session中的数据同步到数据库
                for se_goods in session_goods:
                    # se_goods结构为[goods_id,num,is_select]
                    cart = ShoppingCart.objects.filter(user_id=user_id, goods_id=se_goods[0]).first()
                    if cart:
                        # 更新商品信息
                        if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
                            cart.nums = se_goods[1]
                            cart.is_select = se_goods[2]
                            cart.save()
                    else:
                        # 创建
                        ShoppingCart.objects.create(user_id=user_id, goods_id=se_goods[0],
                                                    nums=se_goods[1], is_select=se_goods[2])
            # 同步数据库的数据到session中
            db_carts = ShoppingCart.objects.filter(user_id=user_id)
            # 组装多个商品格式:[[goods_id,num,is_select],[goods_id,num,is_select]]
            if db_carts:
                new_session_goods = [[cart.goods_id, cart.nums, cart.is_select] for cart in db_carts]
                # result = []
                # for cart in db_carts:
                    # data = [cart.goods_id, cart.num, cart.is_select]
                    # result.append(data)
                request.session['goods'] = new_session_goods
        return response