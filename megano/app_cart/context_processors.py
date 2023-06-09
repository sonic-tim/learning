import re
from typing import Any

from app_cart.models import Cart

regex = r"(\/admin[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"


# Получаем инфу о корзине пользователя на каждой странице
def get_info_about_users_basket(request: Any) -> dict:
    """
    Если текущий URL связан с административной панелью возвращает пустой словарь.
    Возвращает словарь с суммой товаров в корзине и количеством товаров в корзине пользователя.

    :param request: Любой - объект запроса.
    :type request: Any
    :return: Словарь с суммой товаров в корзине и количеством товаров в корзине пользователя.
    """
    if re.search(regex, request.META['PATH_INFO']):
        return {}
    if request.user.id:
        user_cart = request.user.user_cart
        amount = user_cart.amount
        number_of_products = user_cart.number_of_products
    else:
        user_cart = Cart.objects.get(session=request.META.get('CSRF_COOKIE'))
        amount = user_cart.amount
        number_of_products = user_cart.number_of_products
    context = {
        'amount': amount,
        'number_of_products': number_of_products
    }
    return context
