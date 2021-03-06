from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from cart.models import ShoppingCart
from fresh_shop.settings import ORDER_NUMBER
from order.models import OrderInfo, OrderGoods
from user.models import UserAddress
from utils.function import get_order_sn


def place_order(request):
    if request.method == 'GET':
        # 获取当前登陆系统的用户对象
        user = request.user
        carts = ShoppingCart.objects.filter(user=user, is_select=True).all()
        # 计算小计和总价
        total_price = 0
        for cart in carts:
            # 小计金额
            price = cart.goods.shop_price * cart.nums
            # 给cart添加一个小计的属性并赋值
            cart.goods_price = price
            # 总金额
            total_price += price
        # 获取当前登陆系统的用户的收货地址信息
        user_addrss = UserAddress.objects.filter(user=user).all()

        return render(request, 'place_order.html', {'carts': carts, 'total_price': total_price, 'num': len(carts),
                                                    'user_address': user_addrss})


def order(request):
    if request.method == 'POST':
        # 1.获取收货地址值
        ad_id = request.POST.get('ad_id')
        # 2.创建订单
        user_id = request.session.get('user_id')
        # 获取订单编号
        order_sn = get_order_sn()
        shop_cart = ShoppingCart.objects.filter(user_id=user_id,
                                                is_select=True)
        # 计算订单总金额
        order_mount = 0
        for cart in shop_cart:
            order_mount += cart.goods.shop_price * cart.nums
        # 收货信息
        user_address = UserAddress.objects.filter(pk=ad_id).first()
        order = OrderInfo.objects.create(user_id=user_id, order_sn=order_sn,
                                         order_mount=order_mount, address=user_address,
                                         signer_name=user_address.signer_name,
                                         signer_mobile=user_address.signer_mobile)
        # 3.创建订单详情
        for cart in shop_cart:
            OrderGoods.objects.create(order=order, goods=cart.goods,
                                      goods_nums=cart.nums)
        # 4.删除购物车中已结算的商品
        # 删除数据库中的商品
        shop_cart.delete()
        session_goods = request.session.get('goods')
        # 删除session中已选择(结算)的物品
        for se_goods in session_goods[:]:
            # se_goods结果[goods_id, nums, is_select]
            if se_goods[2]:
                session_goods.remove(se_goods)
        request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def user_order(request):
    if request.method == 'GET':
        activate = 'order'
        page = int(request.GET.get('page', 1))
        # 获取登陆系统用户的id值
        user_id = request.session.get('user_id')
        # 查询当前用户产生的订单信息
        orders = OrderInfo.objects.filter(user_id=user_id)
        status = OrderInfo.ORDER_STATUS
        # 分页,ORDER_NUMBER为工程目录中设置的每页显示的信息数量
        pg = Paginator(orders, ORDER_NUMBER)
        my_page = pg.page(page)
        return render(request, 'user_center_order.html', {'orders': my_page, 'status': status, 'activate': activate})