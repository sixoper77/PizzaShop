from decimal import Decimal
from django.conf import settings
from django.core.cache import cache
from main.models import Products

class Cart:
    def __init__(self, request=None, telegram_id=None):
        self.request = request
        
        if telegram_id:
            # Для Telegram пользователей используем кэш
            self.cache_key = f"cart_telegram_{telegram_id}"
            self.telegram_id = telegram_id
            cached_cart = cache.get(self.cache_key)
            if not cached_cart:
                cached_cart = {}
            self.cart = cached_cart
        elif request is not None:
            # Обычная логика для веб-пользователей
            self.session = request.session
            self.cart_key = settings.CART_SESSION_ID
            cart = self.session.get(self.cart_key)
            if not cart:
                self.session[self.cart_key] = {}
            self.cart = self.session[self.cart_key]
        else:
            # Пустая корзина, если нет ни request, ни telegram_id
            self.cart = {}
    
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'discount': float(product.discount) if product.discount else 0.0
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        
    def save(self):
        if hasattr(self, 'cache_key'):
            # Для Telegram пользователей сохраняем в кэш
            cache.set(self.cache_key, self.cart, 3600)
        else:
            # Для веб-пользователей сохраняем в сессию
            self.session.modified = True
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = float(item['price']) 
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self):
        if hasattr(self, 'cache_key'):
            # Для Telegram пользователей очищаем кэш
            self.cart = {}
            cache.set(self.cache_key, {}, 3600)
        else:
            # Для веб-пользователей
            if self.cart_key in self.session:
                del self.session[self.cart_key]
                self.session.modified = True
    
    def get_total_price(self):
        total = sum((float(item['price']) - (float(item['price']) * float(item.get('discount', 0)) / 100)) * item['quantity']
                    for item in self.cart.values())
        return format(round(total,2))
                