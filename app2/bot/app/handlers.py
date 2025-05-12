from aiogram import Router,F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import app.keyboards as kb
from aiogram.fsm.context import FSMContext 
import aiohttp
from aiogram import Router
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.types import InputMediaPhoto
from .data import *
from .state import *
router = Router()
@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer('Привет,это тест бот.\nАвтор данного треша- @sixoper77', reply_markup=kb.menu)
    user_id=message.from_user.id
    username=message.from_user.username or f'tg_{user_id}'
    print(user_id)
    print(username)
    await save_telegram_id(user_id,username)
        
@router.callback_query(F.data=='start')
async def back(callback:CallbackQuery):
    await callback.answer('Главное меню')
    await callback.message.edit_text("Hello", reply_markup=kb.menu)
    
@router.callback_query(F.data == 'Category')
async def catalog(callback: CallbackQuery):
    await callback.answer('')

    if callback.message.text:
        await callback.message.edit_text('Select product category', reply_markup=await kb.categories())
    else:
        await callback.message.answer('Select product category', reply_markup=await kb.categories())
@router.callback_query(F.data=='Products')
async def all_products(callback:CallbackQuery, state:FSMContext):
    await callback.answer('')
    all_products_data = await kb.get_data()
    await state.update_data(products=all_products_data)
    if callback.message.text:
        await callback.message.edit_text('Список всех продуктов', reply_markup=await kb.products())
    else:
        await callback.message.answer('Список всех продуктов', reply_markup=await kb.products())

@router.callback_query(F.data.startswith('category_'))
async def category(callback:CallbackQuery,state: FSMContext):
    await callback.answer('')
    print(callback.data[9:])
    await callback.message.edit_text('выберите продукт по категории',
                                     reply_markup=await kb.get_items_by_category_slug(callback.data[9:],state))
@router.callback_query(F.data.startswith('product_'))
async def item(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    products = data.get('products', [])

    try:
        product_id = int(callback.data.split('_')[1])
    except ValueError:
        await callback.message.answer("Ошибка! Неверный формат данных.")
        return
    product_index = next((i for i, p in enumerate(products) if p["id"] == product_id), None)
    if product_index is None:
        await callback.message.answer("Ошибка! Товар не найден.")
        return

    product = products[product_index]
    image_url = product.get("image_url")

    image_bytes=await get_image_url(image_url)

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=BufferedInputFile(image_bytes, filename="product.jpg"),
            caption=f"🛒 {product['name']}\n💰 Цена: {product['price']}$ \nСостав: {product['description']}"
        ),
        reply_markup=kb.switch_item(product_index,product_id,products)
    )
    
@router.callback_query(F.data.startswith('next_pizza_'))
async def next_pizza(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    products = data.get('products', [])
    try:
        index = int(callback.data.split('_')[2]) + 1
    except ValueError:
        await callback.message.answer("Ошибка! Неверный формат данных.")
        return
    if index < len(products):  
        product = products[index]
        image_url = product.get("image_url")
        image_bytes=await get_image_url(image_url)
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=BufferedInputFile(image_bytes, filename="product.jpg"),
                caption=f"🛒 {product['name']}\n💰 Цена: {product['price']}$\n Состав:{product['description']}"
            ),
            reply_markup=kb.switch_item(index,product['id'],products)
        )
    else:
        await callback.answer('Это последняя пицца')

@router.callback_query(F.data.startswith('back_pizza_'))
async def back_pizza(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    products = data.get('products', [])
    print(products)
    try:
        index = int(callback.data.split('_')[2]) - 1
    except ValueError:
        await callback.message.answer("Ошибка! Неверный формат данных.")
        return
    if index >= 0:
        product = products[index]
        image_url = product.get("image_url")
        image_bytes=await get_image_url(image_url)
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=BufferedInputFile(image_bytes, filename="product.jpg"),
                caption=f"🛒 {product['name']}\n💰 Цена: {product['price']}$ \nСостав:{product['description']}"
            ),
            reply_markup=kb.switch_item(index,product['id'],products)
        )
    else:
        await callback.answer("Это первая пицца!") 

@router.callback_query(F.data.startswith('add_to_cart_'))
async def add_cart(callback:CallbackQuery,state:FSMContext):
    await callback.answer('')
    user_id=callback.from_user.id
    print(f"callback.data: {callback.data}") 
    product_id=int(callback.data[12:])
    print(product_id)
    data=await state.get_data()
    products=data.get('products',[])
    product=next((i for i in products if i['id']==product_id),None)
    if not product:
        await callback.answer('Товара нет звони мне в телефон!!!')
        return
    print(f"Добавляем в корзину: {product}")
    succes=await add_to_cart({'product_id':product_id,'quantity':1,'telegram_id':user_id},user_id)
    print(succes)

    if succes:
        await callback.answer('Товар добавлен в корзину')
        
@router.callback_query(F.data.startswith('clear_cart'))
async def clear_user_cart(callback:CallbackQuery):
    await callback.answer('')
    user_id=callback.from_user.id
    await clear_cart(user_id)
    show=await show_cart(user_id)
    await callback.message.answer('Корзина была очищена\nВНИМАНИЕ ВАША КОРЗИНА ХРАНИТСЯ ЧАС ЕСЛИ ВЫ НИЧЕГО НЕ КУПИЛИ!,\nХРАНИТСЯ ЧАС!',
                                  reply_markup=kb.menu)

@router.callback_query(F.data.startswith('show_cart'))
async def show(callback:CallbackQuery):
    await callback.answer('')
    user_id=callback.from_user.id
    show=await show_cart(user_id)
    messge_text='Ваша корзина:\n'
    for i in show['cart']:
        messge_text+=f'{i['name']} - {i['quantity']}шт. price: {i['total_price']}$\n'
    messge_text+=f'Итог: {show['total_price']}$'
    await callback.message.answer(messge_text,reply_markup=kb.menu)
    
@router.callback_query(F.data.startswith('create_order'))
async def create_order_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    user_id = callback.from_user.id
    cart_data = await show_cart(user_id)
    if not cart_data['cart']:
        await callback.message.answer('Ваша корзина пуста', reply_markup=kb.menu)
        return
    user_data = await state.get_data()
    await state.update_data(first_name=callback.from_user.first_name or '')
    if callback.from_user.last_name:
        await state.update_data(last_name=callback.from_user.last_name)
        await state.set_state(OrderForm.email)
        await callback.message.answer('Пожалуйста, введите ваш email:')
    else:
        await state.set_state(OrderForm.last_name)
        await callback.message.answer('Пожалуйста, введите вашу фамилию:')
@router.message(OrderForm.last_name)
async def process_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(OrderForm.email)
    await message.answer('Пожалуйста, введите ваш email:')

@router.message(OrderForm.email)
async def process_email(message: Message, state: FSMContext):
    if '@' not in message.text:
        await message.answer('Пожалуйста, введите корректный email:')
        return
    await state.update_data(email=message.text)
    await state.set_state(OrderForm.city)
    await message.answer('Пожалуйста, введите ваш город:')

@router.message(OrderForm.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(OrderForm.address)
    await message.answer('Пожалуйста, введите ваш адрес:')

@router.message(OrderForm.address)
async def process_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(OrderForm.postal_code)
    await message.answer('Пожалуйста, введите почтовый индекс:')

@router.message(OrderForm.postal_code)
async def process_postal_code(message: Message, state: FSMContext):
    await state.update_data(postal_code=message.text)
    user_data = await state.get_data()
    user_id = message.from_user.id
    cart_data = await show_cart(user_id)
    total_price = cart_data.get('total_price', 0)
    items_text = "\n".join([f"🍕 {item['name']} - {item['quantity']} шт." for item in cart_data['cart']])
    confirmation_text = (
        f"Пожалуйста, проверьте данные заказа:\n\n"
        f"👤 {user_data['first_name']} {user_data['last_name']}\n"
        f"📧 {user_data['email']}\n"
        f"🏙️ {user_data['city']}\n"
        f"📍 {user_data['address']}\n"
        f"📮 {user_data['postal_code']}\n\n"
        f"🛍 Ваш заказ:\n{items_text}\n\n"
        f"💰 Общая сумма: {total_price} $.\n\n"
        f"Подтверждаете заказ?"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_order"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_order")
        ]
    ])
    await message.answer(confirmation_text, reply_markup=keyboard)
    await state.set_state(None)
@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    user_id = callback.from_user.id
    user_data = await state.get_data()
    cart_data = await show_cart(user_id)
    order_state = {
        'user': user_data.get('user', ''),
        'first_name': user_data.get('first_name', ''),
        'last_name': user_data.get('last_name', ''),
        'email': user_data.get('email', ''),
        'city': user_data.get('city', ''),
        'address': user_data.get('address', ''),
        'postal_code': user_data.get('postal_code', ''),
        'items': [
            {'product_id': item['id'], 'quantity': item['quantity']}
            for item in cart_data['cart']
        ]
    }
    
    try:
        response = await save_telegram_order(order=order_state, user_id=user_id)
        if response.get("status") == "success":
            kb.menu.inline_keyboard.append([InlineKeyboardButton(text='Оплатить', callback_data=f'pay_order_{response['order_id']}')])
            await callback.message.answer(
                f"✅ Ваш заказ успешно создан! Номер заказа: {response['order_id']}\
                Что бы сформировать ссылку оплаты нажмите кнопку Оплатить",
                reply_markup=kb.menu
            )
            await clear_cart(user_id)  
        else:
            error_details = ''
            if isinstance(response.get('message'), dict):
                for field, errors in response['message'].items():
                    error_details += f"\n• {field}: {', '.join(errors)}"
            
            await callback.message.answer(
                f"❌ Ошибка при создании заказа: {response.get('message', 'Неизвестная ошибка')}{error_details}",
                reply_markup=kb.menu
            )
    except Exception as e:
        print(f"Ошибка при подтверждении заказа: {e}")
        await callback.message.answer(
            "❌ Произошла ошибка при обработке заказа. Пожалуйста, попробуйте позже.",
            reply_markup=kb.menu
        )

@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer("Заказ отменен", reply_markup=kb.menu)
    
@router.callback_query(F.data.startswith('pay_order_'))
async def pay(callback:CallbackQuery,state:FSMContext):
    await callback.answer('')
    order_id=callback.data[10:]
    data=await checkout_telegram(order_id)
    await callback.message.answer(
                f"Ссылка для оплаты Готова!",reply_markup=kb.payment_button(data['stripe_url']))