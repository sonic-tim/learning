from datetime import datetime
from typing import Any

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.safestring import mark_safe


# Возвращает полное имя пользователя.
def get_full_name_user(self: Any) -> str:
	"""
	Функция возвращает полное имя пользователя

	:param self: Любой.
	:type self: Any
	:return: Полное имя пользователя.
	"""
	return self.user_profile.full_name


# Добавление метода отображения пользователя в класс User.
User.add_to_class("__str__", get_full_name_user)


# Класс Settings — это модель для конфигурации приложения.
class Settings(models.Model):
	title = models.CharField(
		max_length=50,
		verbose_name='Название интернет-магазина',
		help_text='Megano'
	)
	SERVER_EMAIL = models.EmailField(
		max_length=200,
		verbose_name='Сервер электронной почты',
		help_text='test@test.com'
	)
	EMAIL_USE_TLS = models.BooleanField(
		choices=[(True, True), (False, False)],
		verbose_name='Использование шифрования TLS'
	)
	EMAIL_HOST = models.CharField(
		max_length=200,
		verbose_name='Сервер исходящей почты',
		help_text='smtp.test.com'
	)
	EMAIL_PORT = models.IntegerField(
		verbose_name='Порт исходящей почты',
		help_text='587'
	)
	EMAIL_HOST_USER = models.EmailField(
		max_length=200,
		verbose_name='Адрес электронной почты',
		help_text='test@test.com'
	)
	EMAIL_HOST_PASSWORD = models.CharField(
		max_length=200,
		verbose_name='Пароль электронной почты'
	)
	CURRENT_SITE_CURRENCY = models.CharField(
		max_length=1,
		choices=[
			('$', 'Доллар'),
			('€', 'Евро'),
			('₽', 'Рубль')
		],
		verbose_name='Используемая валюта расчетов'
	)
	ALLOWED_HOSTS = models.CharField(
		max_length=100,
		verbose_name='Разрешенный хост',
		help_text='example.com или 0.0.0.0'
	)

	class Meta:
		db_table = 'settings'
		verbose_name = 'настройки сайта'
		verbose_name_plural = 'настройки сайта'

	def __str__(self):
		return self.title


# Класс Profile — это модель, которая хранит в себе расширенную информацию о пользователе
class Profile(models.Model):
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		verbose_name='пользователь',
		related_name='user_profile'
	)
	phone = models.CharField(
		max_length=10,
		verbose_name='номер телефона',
		help_text='Номер телефона в формате 9998887766'
	)
	full_name = models.CharField(
		null=True,
		blank=True,
		max_length=100,
		verbose_name='полное имя'
	)
	user_photo = models.ImageField(
		null=True,
		blank=True,
		upload_to='profile',
		verbose_name='фото пользователя'
	)

	# Функция, которая возвращает тег изображения для поля user_photo.
	def image_tag(self: Any) -> str:
		"""
		Метод возвращает строку, содержащую HTML-тег изображения.

		:param self: Любой — это объект, который передается функции.
		:type self: Any
		:return: Тег с URL-адресом изображения.
		"""
		return mark_safe('<img src="%s" style="height:30px;" />' % self.user_photo.url)

	image_tag.short_description = 'Image'

	class Meta:
		db_table = 'profile'
		verbose_name = 'профиль пользователя'
		verbose_name_plural = 'профили пользователей'

	def __str__(self):
		return self.user.email


# Класс Category — это модель, которая хранит в себе информацию о категориях товаров.
class Category(models.Model):
	title = models.CharField(
		max_length=50,
		verbose_name='название категории'
	)
	image = models.ImageField(
		upload_to='categories',
		verbose_name='изображение категории'
	)

	def image_tag(self):
		"""
		Метод возвращает строку, содержащую HTML-тег изображения.

		:param self: Любой — это объект, который передается функции.
		:type self: Any
		:return: Тег с URL-адресом изображения.
		"""
		return mark_safe('<img src="%s" style="height:30px;" />' % self.image.url)

	image_tag.short_description = 'Image'

	# Возврат URL-адреса объекта.
	def get_absolute_url(self: Any) -> str:
		"""
		Функция возвращает URL-адрес для доступа к конкретному экземпляру модели.

		:param self: Любой
		:type self: Any
		:return: URL-адрес подробного представления категории товаров.
		"""
		return reverse('category_detail', args=[str(self.id)])

	class Meta:
		db_table = 'category'
		verbose_name = 'категория'
		verbose_name_plural = 'категории'

	def __str__(self):
		return self.title


# Класс Subcategory — это модель, которая хранит в себе информацию о подкатегориях товаров.
class Subcategory(models.Model):
	# Создание отношения внешнего ключа между моделью подкатегории и моделью категории.
	category = models.ForeignKey(
		Category,
		on_delete=models.CASCADE,
		verbose_name='категория',
		related_name='subcategories'
	)
	title = models.CharField(
		max_length=50,
		verbose_name='название подкатегории'
	)
	image = models.ImageField(
		upload_to='categories',
		verbose_name='изображение подкатегории'
	)

	def image_tag(self):
		"""
		Метод возвращает строку, содержащую HTML-тег изображения.

		:param self: Любой — это объект, который передается функции.
		:type self: Any
		:return: Тег с URL-адресом изображения.
		"""
		return mark_safe('<img src="%s" style="height:30px;" />' % self.image.url)

	image_tag.short_description = 'Image'

	# Возврат URL-адреса объекта.
	def get_absolute_url(self: Any) -> str:
		"""
		Функция возвращает URL-адрес для доступа к конкретному экземпляру модели.

		:param self: Любой
		:type self: Any
		:return: URL-адрес подробного представления подкатегории товаров.
		"""
		return reverse('subcategory_detail', args=[str(self.category.id), str(self.id)])

	class Meta:
		db_table = 'subcategory'
		verbose_name = 'подкатегория'
		verbose_name_plural = 'подкатегории'

	def __str__(self):
		return '%s (%s)' % (self.title, self.category)


# Класс OrderStatus — это модель, которая хранит в себе список статусов заказа.
class OrderStatus(models.Model):
	title = models.CharField(
		max_length=30,
		verbose_name='статус заказа'
	)

	class Meta:
		db_table = 'order_status'
		verbose_name = 'статус заказа'
		verbose_name_plural = 'статусы заказов'

	def __str__(self):
		return self.title


# Класс DeliveryType — это модель, которая хранит в себе доступные варианты доставки.
class DeliveryType(models.Model):
	title = models.CharField(
		max_length=30,
		verbose_name='тип доставки'
	)
	free_delivery = models.BooleanField(
		null=True,
		blank=True,
		default=False,
		choices=((True, 'Доступна'), (False, 'Недоступна'),),
		verbose_name='возможность бесплатной доставки'
	)
	purchase_amount_for_free_delivery = models.IntegerField(
		verbose_name='минимальная сумма заказа для бесплатной доставки',
		null=True,
		blank=True
	)
	delivery_cost = models.IntegerField(
		verbose_name='стоимость платной доставки'
	)

	class Meta:
		db_table = 'delivery_type'
		verbose_name = 'тип доставки'
		verbose_name_plural = 'типы доставки'

	def __str__(self):
		return self.title

# Класс PaymentMethod — это модель, которая хранит в себе доступные варианты оплаты.
class PaymentMethod(models.Model):
	title = models.CharField(
		max_length=30,
		verbose_name='способ оплаты'
	)

	class Meta:
		db_table = 'payment_method'
		verbose_name = 'способ оплаты'
		verbose_name_plural = 'способы оплаты'

	def __str__(self):
		return self.title

# Класс Promotion — это модель, которая хранит в себе информацию об акциях в магазине.
class Promotion(models.Model):
	title = models.CharField(
		max_length=100,
		verbose_name='название акции'
	)
	description = models.TextField(
		verbose_name='описание акции'
	)
	is_active = models.BooleanField(
		default=False,
		blank=True,
		null=True,
		verbose_name='статус активности'
	)
	discount_size = models.FloatField(
		validators=[MinValueValidator(0), MaxValueValidator(100)],
		verbose_name='размер скидки'
	)
	promo_start_date = models.DateField(
		blank=True,
		null=True,
		verbose_name='дата начала акции'
	)
	promo_end_date = models.DateField(
		blank=True,
		null=True,
		verbose_name='дата окончания акции',
	)

	class Meta:
		db_table = 'promotion'
		ordering = ['promo_end_date']
		verbose_name = 'акция'
		verbose_name_plural = 'акции'

	def __init__(self, *args, **kwargs):
		"""
		Если promo_end_date меньше сегодняшней даты или promo_start_date больше сегодняшней даты, то акция не активна. В
		противном случае она активен
		"""
		super().__init__(*args, **kwargs)
		if self.id:
			if self.promo_end_date < datetime.today().date() or self.promo_start_date > datetime.today().date():
				self.is_active = False
			else:
				self.is_active = True
			self.save(update_fields=['is_active'])

	# Возврат URL-адреса объекта.
	def get_absolute_url(self: Any) -> str:
		"""
		Функция возвращает URL-адрес для доступа к конкретному экземпляру модели.

		:param self: Любой
		:type self: Any
		:return: URL-адрес подробного представления рекламной акции.
		"""
		return reverse('promotion_detail', args=[str(self.id)])

	def __str__(self):
		return self.title


# Класс DeliveryType — это модель, которая хранит в себе информацию и типе характеристики товара и единице измерения
# характеристики.
class Specification(models.Model):
	title = models.CharField(
		max_length=100,
		verbose_name='название'
	)
	unit = models.CharField(
		max_length=10,
		null=True,
		blank=True,
		verbose_name='единицы измерения'
	)

	class Meta:
		db_table = 'specifications'
		verbose_name = 'характеристика'
		verbose_name_plural = 'характеристики'

	def __str__(self):
		return '%s (%s)' % (self.title, self.unit if self.unit else '-')


# Класс Tag — это модель, которая хранит в себе название тега и количество запросов по данному тегу.
class Tag(models.Model):
	title = models.CharField(
		max_length=20,
		unique=True,
		verbose_name='тег'
	)
	number_of_requests = models.IntegerField(
		default=0,
		null=True,
		blank=True,
		verbose_name='количество запросов по тегу'
	)

	# Возврат URL-адреса объекта.
	def get_absolute_url(self: Any) -> str:
		"""
		Функция возвращает URL-адрес для доступа к конкретному экземпляру модели.

		:param self: Любой
		:type self: Any
		:return: URL-адрес подробного представления тега.
		"""
		return reverse('tag_detail', args=[str(self.id)])

	class Meta:
		db_table = 'tag'
		verbose_name = 'тег'
		verbose_name_plural = 'теги'

	def __str__(self):
		return self.title


# Класс KeyFeature - это модель, которая хранит в себе ключевые особенности товаров.
class KeyFeature(models.Model):
	list_item = models.CharField(
		max_length=100,
		null=False,
		blank=False,
		verbose_name='наименование пункта'
	)
	description = models.TextField(
		null=False,
		blank=False,
		verbose_name='описание'
	)

	class Meta:
		db_table = 'key_feature'
		verbose_name = 'ключевая особенность'
		verbose_name_plural = 'ключевые особенности'

	def __str__(self):
		return self.list_item[:20]


# Класс AddInfo - это модель, которая хранит в себе список значений дополнительной информации о товаре.
class AddInfo(models.Model):
	list_item = models.CharField(
		max_length=50,
		null=False,
		blank=False,
		verbose_name='наименование пункта'
	)

	class Meta:
		db_table = 'add_info'
		verbose_name = 'дополнительная информация'
		verbose_name_plural = 'дополнительная информация'

	def __str__(self):
		return self.list_item[:20]


# Класс Cart - это модель, которая хранит в себе информацию о корзине пользователя.
class Cart(models.Model):
	user = models.OneToOneField(
		User,
		null=True,
		blank=True,
		on_delete=models.CASCADE,
		verbose_name='пользователь',
		related_name='user_cart'
	)
	session = models.CharField(
		max_length=150,
		verbose_name='ключ сессии'
	)
	amount = models.FloatField(
		null=True,
		blank=True,
		verbose_name='сумма товаров в корзине'
	)
	number_of_goods = models.IntegerField(
		null=True,
		blank=True,
		verbose_name='количество товаров в корзине'
	)

	class Meta:
		db_table = 'cart'
		verbose_name = 'корзина'
		verbose_name_plural = 'корзины'

	def __init__(self: Any, *args, **kwargs) -> None:
		"""
		Обновляет количество товаров и сумму в корзине при добавлении нового товара в корзину.

		:param self: Любой — это экземпляр сохраняемой модели.
		:type self: Any
		"""
		super().__init__(*args, **kwargs)
		try:
			# Проверяем, пуста ли корзина.
			if not self.goods_in_carts:
				raise ObjectDoesNotExist
			# Использование агрегатной функции для суммирования количества всех товаров в корзине.
			self.number_of_goods = self.goods_in_carts.all().aggregate(Sum('quantity'))['quantity__sum']
			# Использование агрегатной функции для суммирования стоимости товаров в корзине.
			self.amount = self.goods_in_carts.all().aggregate(Sum('amount'))['amount__sum']
			# Обновление полей количество товаров и суммы в базе.
			self.save(update_fields=['number_of_goods', 'amount'])
		except ObjectDoesNotExist:
			self.number_of_goods = 0
			self.amount = 0
			self.save(update_fields=['number_of_goods', 'amount'])

	def __str__(self):
		return '%s [user:%s]' % (self.session, self.user)


# Класс Good - это модель, которая хранит в себе информацию о товарах в магазине.
class Good(models.Model):
	category = models.ForeignKey(
		Subcategory,
		on_delete=models.CASCADE,
		verbose_name='категория товара',
		related_name='category_goods'
	)
	sku = models.CharField(
		max_length=12,
		null=False,
		blank=False,
		unique=True,
		verbose_name='артикул'
	)
	barcode = models.CharField(
		max_length=15,
		null=False,
		blank=False,
		unique=True,
		verbose_name='штрихкод'
	)
	title = models.CharField(
		max_length=100,
		verbose_name='наименование товара'
	)
	description = models.TextField(
		verbose_name='описание товара'
	)
	price = models.FloatField(
		verbose_name='цена'
	)
	current_price = models.FloatField(
		null=True,
		blank=True,
		verbose_name='текущая цена'
	)
	quantity = models.IntegerField(
		null=False,
		blank=False,
		validators=[MinValueValidator(0)],
		verbose_name='количество товара на складе'
	)
	promotion = models.ForeignKey(
		Promotion,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='goods_on_sale',
		verbose_name='участвует в акции'
	)
	main_photo = models.ImageField(
		upload_to='good',
		verbose_name='главное фото товара'
	)
	is_limited = models.BooleanField(
		null=True,
		blank=True,
		default=False,
		verbose_name='ограниченный тираж'
	)

	class Meta:
		db_table = 'good'
		ordering = ['current_price']
		verbose_name = 'товар'
		verbose_name_plural = 'товары'

	def image_tag(self):
		"""
		Метод возвращает строку, содержащую HTML-тег изображения.

		:param self: Любой — это объект, который передается функции.
		:type self: Any
		:return: Тег с URL-адресом изображения.
		"""
		return mark_safe('<img src="%s" style="height:30px;" />' % self.main_photo.url)

	image_tag.short_description = 'Image'

	def __init__(self: Any, *args, **kwargs) -> None:
		"""
		Если у товара есть идентификатор и акция, и акция активна, то текущая цена равна цене минус цена, умноженная на
		размер скидки по акции.

		:param self: Любой — это экземпляр сохраняемой модели.
		:type self: Any
		"""
		super().__init__(*args, **kwargs)
		if self.id:
			if self.promotion:
				if not self.promotion.is_active:
					self.promotion = None
					self.save(update_fields=['promotion'])
			if self.promotion:
				self.current_price = round(self.price - (self.price * self.promotion.discount_size / 100), 0)
			else:
				self.current_price = self.price
			self.save(update_fields=['current_price'])

	# Возврат URL-адреса объекта.
	def get_absolute_url(self: Any) -> str:
		"""
		Функция возвращает URL-адрес для доступа к конкретному экземпляру модели.

		:param self: Любой
		:type self: Any
		:return: URL-адрес подробного представления товара.
		"""
		return reverse('product', args=[str(self.id)])

	def __str__(self):
		return '%s %s %s' % (self.category, self.title, self.current_price)


# Класс AddGoodPhoto - это модель, которая хранит в себе дополнительные фотографии товара.
class AddGoodPhoto(models.Model):
	good = models.ForeignKey(
		Good,
		on_delete=models.CASCADE,
		related_name='photo_gallery',
		verbose_name='товар'
	)
	photo = models.ImageField(
		upload_to='good_gallery',
		verbose_name='фото товара'
	)

	class Meta:
		db_table = 'add_good_photo'
		verbose_name = 'фотография товара'
		verbose_name_plural = 'фотографии товара'

	def image_tag(self):
		"""
		Метод возвращает строку, содержащую HTML-тег изображения.

		:param self: Любой — это объект, который передается функции.
		:type self: Any
		:return: Тег с URL-адресом изображения.
		"""
		return mark_safe('<img src="%s" style="height:30px;" />' % self.photo.url)

	image_tag.short_description = 'Image'
	image_tag.allow_tags = True


# Класс Review - это модель, которая хранит в себе информацию об отзывах о товаре.
class Review(models.Model):
	good = models.ForeignKey(
		Good,
		on_delete=models.CASCADE,
		verbose_name='товар',
		related_name='good_reviews'
	)
	full_name = models.CharField(
		max_length=100,
		verbose_name='ФИО'
	)
	email = models.EmailField(
		verbose_name='электронная почта'
	)
	user_photo = models.CharField(
		max_length=200,
		null=True,
		blank=True,
		verbose_name='фото пользователя'
	)
	text = models.TextField(
		verbose_name='отзыв'
	)
	creation_date = models.DateTimeField(
		auto_now_add=True,
		verbose_name='дата отзыва'
	)

	class Meta:
		db_table = 'review'
		ordering = ['good']
		verbose_name = 'отзыв на товар'
		verbose_name_plural = 'отзывы на товар'

	def __str__(self):
		return self.good.title


# Класс GoodSpecification - это модель, которая хранит в себе информацию о характеристиках товара.
class GoodSpecification(models.Model):
	good = models.ForeignKey(
		Good,
		on_delete=models.CASCADE,
		verbose_name='товар',
		related_name='good_specifications'
	)
	# Создание внешнего ключа к модели спецификации.
	specification = models.ForeignKey(
		Specification,
		on_delete=models.CASCADE,
		verbose_name='характеристика'
	)
	value = models.CharField(
		max_length=100,
		verbose_name='значение'
	)

	class Meta:
		db_table = 'good_specification'
		verbose_name = 'характеристика товара'
		verbose_name_plural = 'характеристики товаров'

	def __str__(self):
		return '%s: %s - %s' % (self.good.title, self.specification, self.value)


# Класс GoodTag - это модель, которая хранит в себе информацию о тегах товара.
class GoodTag(models.Model):
	good = models.ForeignKey(
		Good,
		on_delete=models.CASCADE,
		verbose_name='товар',
		related_name='good_tags'
	)
	tag = models.ForeignKey(
		Tag,
		on_delete=models.CASCADE,
		verbose_name='тег',
		related_name='goods_by_tags'
	)

	class Meta:
		db_table = 'good_tag'
		verbose_name = 'тег товара'
		verbose_name_plural = 'теги товаров'

	def __str__(self):
		return self.tag.title


# Класс KeyGoodFeature - это модель, которая хранит в себе информацию о ключевых особенностях товара.
class KeyGoodFeature(models.Model):
	good = models.ForeignKey(
		Good,
		on_delete=models.CASCADE,
		related_name='key_good_features',
		verbose_name='товар'
	)
	key_feature = models.ForeignKey(
		KeyFeature,
		on_delete=models.CASCADE,
		related_name='good_with_key_features',
		verbose_name='ключевая особенность'
	)

	class Meta:
		db_table = 'key_good_feature'
		verbose_name = 'ключевая особенность товара'
		verbose_name_plural = 'ключевые особенности товара'

	def __str__(self):
		return '%s (%s)' % (self.key_feature, self.good.title)


# Класс AddGoodInfo - это модель, которая хранит в себе информацию о дополнительной информации о товаре.
class AddGoodInfo(models.Model):
	good = models.ForeignKey(
		Good,
		on_delete=models.CASCADE,
		verbose_name='товар',
		related_name='add_info_about_good'
	)
	add_info = models.ForeignKey(
		AddInfo,
		on_delete=models.CASCADE,
		verbose_name='наименование пункта'
	)
	value = models.CharField(
		max_length=100,
		verbose_name='значение'
	)

	class Meta:
		db_table = 'add_good_info'
		verbose_name = 'дополнительная информация о товаре'
		verbose_name_plural = 'дополнительные информации о товаре'

	def __str__(self):
		return '%s: %s - %s' % (self.good.title, self.add_info, self.value)


# Класс Order - это модель, которая хранит в себе информацию о заказах покупателей.
class Order(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='user_orders',
		verbose_name='пользователь'
	)
	date_create = models.DateTimeField(
		auto_now_add=True,
		verbose_name='дата заказа'
	)
	delivery_type = models.ForeignKey(
		DeliveryType,
		on_delete=models.CASCADE,
		verbose_name='тип доставки',
		related_name='orders_with_delivery_type'
	)
	city = models.CharField(
		max_length=100,
		verbose_name='город доставки'
	)
	address = models.TextField(
		verbose_name='адрес доставки'
	)
	payment_method = models.ForeignKey(
		PaymentMethod,
		on_delete=models.CASCADE,
		verbose_name='способ оплаты',
		related_name='orders_with_payment_method'
	)
	status = models.ForeignKey(
		OrderStatus,
		on_delete=models.CASCADE,
		default=1,
		verbose_name='статус заказ',
		related_name='orders_with_status'
	)
	payment_error = models.CharField(
		max_length=50,
		null=True,
		blank=True,
		verbose_name='ошибка при оплате'
	)
	payment_error_message = models.CharField(
		max_length=200,
		null=True,
		blank=True,
		verbose_name='сообщение об ошибке при оплате'
	)
	order_amount = models.FloatField(
		verbose_name='сумма заказа',
		blank=True,
		null=True,
	)

	class Meta:
		db_table = 'order'
		ordering = ['-date_create']
		verbose_name = 'заказ'
		verbose_name_plural = 'заказы'

	def __str__(self):
		return '№%(id)s | %(date)s - %(status)s' % {
			'id': self.id,
			'date': self.date_create.strftime('%d.%m.%Y - %H:%M:%S'),
			'status': self.status
		}


# Класс GoodInCart - это модель, которая хранит в себе информацию о товарах в корзине.
class GoodInCart(models.Model):
	cart = models.ForeignKey(
		Cart,
		on_delete=models.CASCADE,
		verbose_name='корзина',
		related_name='goods_in_carts'
	)
	good = models.ForeignKey(
		Good,
		on_delete=models.CASCADE,
		verbose_name='товар',
		related_name='added_goods'
	)
	quantity = models.IntegerField(
		verbose_name='количество',
		validators=[MinValueValidator(0)]
	)
	amount = models.FloatField(
		verbose_name='сумма',
		null=True,
		blank=True
	)

	class Meta:
		db_table = 'good_in_cart'
		verbose_name = 'товар в корзине'
		verbose_name_plural = 'товары в корзине'

	def __init__(self: Any, *args, **kwargs) -> None:
		"""
		Если id объекта существует, то рассчитываем сумму товара в корзине.

		:param self: Любой — это экземпляр сохраняемой модели.
		:type self: Any
		"""
		super().__init__(*args, **kwargs)
		if self.id:
			self.amount = self.quantity * self.good.current_price
			self.save(update_fields=['amount'])

	def __str__(self):
		return self.good.title


# Класс GoodInOrder - это модель, которая хранит в себе информацию о товарах в заказе.
class GoodInOrder(models.Model):
	order = models.ForeignKey(
		Order,
		null=True,
		on_delete=models.SET_NULL,
		verbose_name='заказ',
		related_name='goods_in_order'
	)
	good = models.ForeignKey(
		Good,
		on_delete=models.CASCADE,
		verbose_name='товар',
		related_name='ordered_goods'
	)
	price = models.FloatField(
		verbose_name='цена товара'
	)
	quantity = models.IntegerField(
		verbose_name='количество'
	)
	amount = models.FloatField(
		verbose_name='сумма',
		null=True,
		blank=True
	)

	class Meta:
		db_table = 'good_in_order'
		verbose_name = 'товар в заказе'
		verbose_name_plural = 'товары в заказе'

	def __init__(self: Any, *args, **kwargs) -> None:
		"""
		Если id объекта не None, то вычисляем сумму товара в заказе

		:param self: Любой — это экземпляр сохраняемой модели
		:type self: Any
		"""
		super().__init__(*args, **kwargs)
		if self.id:
			self.amount = self.quantity * self.price
			self.save(update_fields=['amount'])

	def __str__(self):
		return self.good.title
