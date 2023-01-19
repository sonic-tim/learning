from random import sample
from typing import Any

from django.core.paginator import Paginator
from django.db.models import Count, Sum, Q, Min, Max
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View, DetailView, ListView

from app_cart.models import Cart
from app_order.models import DeliveryType
from app_shop.forms import ReviewForm
from app_shop.models import Good, Subcategory, Category, Tag


def about(request: Any) -> HttpResponse:
	"""
	Функция возвращает обработанный шаблон "О магазине".

	:param request: Это объект запроса, который Django использует для передачи информации из браузера на сервер
	:type request: Any
	:return: Объект HttpResponse.
	"""
	return render(
		request,
		'app_shop/about.html'
	)


def add_review(request: Any, pk: str) -> HttpResponse:
	"""
	Функция принимает запрос и идентификатор продукта, добавляет отзыв о товаре и перенаправляет на страницу продукта.

	:param request: Объект запроса является первым параметром любой функции представления. Он содержит информацию о
	запросе, который был сделан на сервер.
	:type request: Any
	:param pk: Первичный ключ продукта, к которому добавляется отзыв.
	:type pk: str
	:return: HttpResponseRedirect (страница товара) или с формой отзыва.
	"""
	form = ReviewForm(request.POST)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect('/product/%s/' % pk)
	form = ReviewForm()
	return HttpResponseRedirect('/product/%s/' % pk, {'form': form})


# Функция используется всеми представлениями, которые используют шаблон catalog.html.
def sort_of_good(self: Any, context: dict, object_list: Any) -> dict:
	"""
	Сортирует товары по выбранному параметру, обрабатывает фильтры и возвращает контекст с отсортированными и/или
	отфильтрованными товарами.

	:param self: Любой
	:type self: Any
	:param context: словарь переменных контекста, которые будут переданы в шаблон.
	:type context: dict
	:param object_list: список объектов, которые вы хотите разбить на страницы.
	:type object_list: Any
	:return: Словарь.
	"""
	# Установите для переменных number_of_clicks и sort значение по умолчанию.
	number_of_clicks = 0
	sort = None
	# Получение значения нажатой кнопки.
	button = self.request.GET.get('button')
	# Передаем значение нажатой кнопки контексту для дальнейшего использования в случае перехода по пагинатору.
	context['button'] = button
	# Проверяется, есть ли в запросе GET значение для ключей ниже, и если да, то преобразуется его в целое число и
	# присваивается переменным. Если это не так, присваивается 0 переменным.
	context['number_of_clicks_popular'] = 0 if not self.request.GET.get('number_of_clicks_popular') else int(
		self.request.GET.get('number_of_clicks_popular')
	)
	context['number_of_clicks_price'] = 0 if not self.request.GET.get('number_of_clicks_price') else int(
		self.request.GET.get('number_of_clicks_price')
	)
	context['number_of_clicks_novelty'] = 0 if not self.request.GET.get('number_of_clicks_novelty') else int(
		self.request.GET.get('number_of_clicks_novelty')
	)
	context['number_of_clicks_review'] = 0 if not self.request.GET.get('number_of_clicks_review') else int(
		self.request.GET.get('number_of_clicks_review')
	)
	# Получение значения списка активных фильтров из словаря request.GET.
	active_filter = self.request.GET.get('active_filter')
	# Получение номера страницы из запроса.
	page_number = self.request.GET.get('page')
	# Получение требования на сохранение сортировки списка товаров.
	is_non_sorted = self.request.GET.get('non_sorted')
	if active_filter:
		active_filter = active_filter.split(',')
	# Фильтрация товаров по параметрам фильтра.
	if button == 'filter' or active_filter:
		if active_filter:
			title, min_price, max_price, is_availability, is_free_delivery = active_filter
			min_price, max_price = float(min_price), float(max_price)
			context['active_filter'] = active_filter
		else:
			title = self.request.GET.get('title')
			min_price, max_price = list(map(float, self.request.GET.get('price').split(';')))
			is_availability = self.request.GET.get('is_availability')
			is_free_delivery = self.request.GET.get('is_free_delivery')
		context['active_filter'] = '%s,%s,%s,%s,%s' % (title, min_price, max_price, is_availability, is_free_delivery)
		if title:
			object_list = object_list.filter(title__icontains=title)
		else:
			object_list = object_list.filter(current_price__gte=min_price, current_price__lte=max_price)
		if is_availability == 'on':
			object_list.filter(quantity__gt=0)
		if is_free_delivery == 'on':
			min_order = DeliveryType.objects.filter(free_delivery=True).first().purchase_amount_for_free_delivery
			object_list.filter(current_price__gt=min_order)
	# Сортировка товаров по нажатой кнопке.
	if button == 'popularity':
		sort = 'ordered_goods__quantity'
		number_of_clicks = context['number_of_clicks_popular'] + (0 if is_non_sorted else 1)
		context['number_of_clicks_popular'] = number_of_clicks
	elif button == 'price':
		sort = 'current_price'
		number_of_clicks = context['number_of_clicks_price'] + (0 if is_non_sorted else 1)
		context['number_of_clicks_price'] = number_of_clicks
	elif button == 'novelty':
		sort = 'id'
		number_of_clicks = context['number_of_clicks_novelty'] + (0 if is_non_sorted else 1)
		context['number_of_clicks_novelty'] = number_of_clicks
	elif button == 'review':
		sort = 'good_reviews__count'
		number_of_clicks = context['number_of_clicks_review'] + (0 if is_non_sorted else 1)
		context['number_of_clicks_review'] = number_of_clicks
	if sort:
		if number_of_clicks % 2 != 0:
			if button == 'novelty':
				object_list = object_list.order_by('-%s' % sort)
			else:
				object_list = object_list.order_by('%s' % sort)
		else:
			if button == 'novelty':
				object_list = object_list.order_by('%s' % sort)
			else:
				object_list = object_list.order_by('-%s' % sort)
	# Передача обновленных данных контексту.
	context['object_list'] = object_list
	context['min_price'] = str(object_list.aggregate(Min('current_price'))['current_price__min']).replace(' ', '')
	context['max_price'] = str(object_list.aggregate(Max('current_price'))['current_price__max']).replace(' ', '')
	paginator = Paginator(object_list, 8)
	page_obj = paginator.get_page(page_number)
	context['paginator'] = paginator
	context['page_obj'] = page_obj
	return context


# Это представление, которое отображает Главную страницу.
class IndexView(View):

	@classmethod
	def get(cls, request: Any) -> HttpResponse:
		"""
		Отображает главную страницу магазина.

		:param cls: Класс представления.
		:param request: Любой - объект запроса
		:type request: Any
		:return: ответ на запрос.
		"""
		# Получение токена CSRF из запроса для связки устройства с корзиной.
		session_id = request.META.get('CSRF_COOKIE')
		# Проверка, авторизован пользователь или нет. Если пользователь не вошел в систему, проверяется существование
		# корзины с текущим токеном, если такой корзины не существует, будет создана новая корзина с текущим токеном.
		if not request.user.id:
			if not Cart.objects.filter(session=session_id):
				Cart.objects.create(session=session_id)
		# Получение случайной выборки из 3 категорий из набора запросов категорий.
		categories = Subcategory.objects.annotate(Count('category_goods')).filter(category_goods__count__gt=0)
		random_number = sample([item.id for item in categories], 3)
		featured_categories = categories.filter(id__in=random_number)
		# Фильтрация товаров по количеству больше 0, затем аннотируется сумма сколько раз заказали товар,
		# а затем упорядочиваются объекты по сумме количества заказанных товаров в порядке убывания.
		popular_good_list = (
			Good.objects.filter(quantity__gt=0)
			.annotate(Sum('ordered_goods__quantity'))
			.order_by('-ordered_goods__quantity__sum')[:8]
		)
		# Фильтрация товаров по количеству больше 0 и статусу лимитированности версии.
		limited_good_list = Good.objects.filter(quantity__gt=0, is_limited=True)[:16]
		return render(
			request,
			'app_shop/index.html',
			context={
				'featured_categories': featured_categories,
				'popular_good_list': popular_good_list,
				'limited_good_list': limited_good_list
			}
		)


class SearchGoodListView(ListView):
	template_name = 'app_shop/catalog.html'
	model = Good

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		query = self.request.GET.get('query')
		object_list = context['object_list'].filter(
			quantity__gt=0,
			title__icontains=query,
		) | Good.objects.filter(
			quantity__gt=0,
			good_tags__tag__title__icontains=query
		)
		tag_list = Tag.objects.filter(title__icontains=query)
		for tag in tag_list:
			if tag.number_of_requests:
				tag.number_of_requests += 1
			else:
				tag.number_of_requests = 1
			tag.save(update_fields=['number_of_requests'])
		context = sort_of_good(self, context, object_list)
		return context


class CategoryDetailView(DetailView):
	template_name = 'app_shop/catalog.html'
	model = Category

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		good_in_category = (
			context['object']
			.subcategories
			.values('category_goods')
			.filter(~Q(category_goods=None))
		)
		object_list = Good.objects.filter(id__in=good_in_category, quantity__gt=0)
		context = sort_of_good(self, context, object_list)
		return context


class SubcategoryDetailView(DetailView):
	template_name = 'app_shop/catalog.html'
	model = Subcategory

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		good_in_subcategory = (
			context['object']
			.category_goods
			.filter(~Q(quantity=0))
		)
		object_list = Good.objects.filter(id__in=good_in_subcategory)
		context = sort_of_good(self, context, object_list)
		return context


class CatalogListView(ListView):
	template_name = 'app_shop/catalog.html'
	model = Good

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		object_list = context['object_list']
		context = sort_of_good(self, context, object_list)
		return context


class TagDetailView(DetailView):
	template_name = 'app_shop/catalog.html'
	model = Tag

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		goods_by_tag = context['object'].goods_by_tags.filter(good__quantity__gt=0)
		object_list = Good.objects.filter(good_tags__in=goods_by_tag, quantity__gt=0)
		context = sort_of_good(self, context, object_list)
		return context


class ProductDetailView(DetailView):
	template_name = 'app_shop/product.html'
	model = Good

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		good = context['object']
		context['specification_list'] = good.good_specifications.all()
		context['key_feature_list'] = good.key_good_features.all()
		context['add_info_list'] = good.add_info_about_good.all()
		try:
			context['review_list'] = good.product_reviews.all()
		except AttributeError:
			context['review_list'] = None
		context['photo_gallery_list'] = good.photo_gallery.all()
		context['tag_list'] = good.good_tags.all()
		if self.request.user.id:
			user_profile = self.request.user.user_profile
			context['form'] = ReviewForm(initial={
				'good': good,
				'email': self.request.user.email,
				'full_name': user_profile.full_name,
				'user_photo': user_profile.user_photo.url if user_profile.user_photo else None
			})
		return context


class PromotionListView(ListView):
	template_name = 'app_shop/sale.html'
	queryset = Good.objects.filter(~Q(promotion=None)).order_by('promotion__promo_end_date')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		object_list = context['object_list']
		page_number = self.request.GET.get('page')
		paginator = Paginator(object_list, 8)
		page_obj = paginator.get_page(page_number)
		context['paginator'] = paginator
		context['page_obj'] = page_obj
		return context
