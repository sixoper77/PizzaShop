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
from .data import add_to_cart,show_cart,save_telegram_id,clear_cart
router = Router()

@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer('Привет дружище,это тест бот.\nАвтор данного треша- @sixoper77', reply_markup=kb.menu)
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

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                image_bytes = await response.read()
            else:
                await callback.message.answer("Ошибка загрузки изображения")
                return

    
    keyboard_buttons = [[InlineKeyboardButton(text='Назад', callback_data='Category')]]
    if product_index > 0:
        prev_product_id = products[product_index - 1]["id"]
        keyboard_buttons.append([InlineKeyboardButton(text='Прошлая пицца', callback_data=f'product_{prev_product_id}')])
    if product_index < len(products) - 1:
        next_product_id = products[product_index + 1]["id"]
        keyboard_buttons.append([InlineKeyboardButton(text='Следующая пицца', callback_data=f'product_{next_product_id}')])

    keyboard_buttons.append([InlineKeyboardButton(text='🛒 Добавить в корзину', callback_data=f'add_to_cart_{product_id}')])
    keyboard_buttons.append([InlineKeyboardButton(text='Просмотреть корзину', callback_data='show_cart')])
    keyboard_buttons.append([InlineKeyboardButton(text='Почистить корзину', callback_data='clear_cart')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=BufferedInputFile(image_bytes, filename="product.jpg"),
            caption=f"🛒 {product['name']}\n💰 Цена: {product['price']}$ \nСостав: {product['description']}"
        ),
        reply_markup=keyboard
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
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_bytes = await response.read()
                else:
                    await callback.message.answer("Ошибка загрузки изображения")
                    return

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data='Category')],
            [InlineKeyboardButton(text='Следующая пицца', callback_data=f'next_pizza_{index}')],
            [InlineKeyboardButton(text='Прошлая пицца', callback_data=f'back_pizza_{index}')],
            [InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_to_cart_{product['id']}')],
            [InlineKeyboardButton(text='Просмотреть корзину', callback_data='show_cart')],
            [InlineKeyboardButton(text='Почистить корзину', callback_data='clear_cart')]
            
        ])
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=BufferedInputFile(image_bytes, filename="product.jpg"),
                caption=f"🛒 {product['name']}\n💰 Цена: {product['price']}$\n Состав:{product['description']}"
            ),
            reply_markup=keyboard
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

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_bytes = await response.read()
                else:
                    await callback.message.answer("Ошибка загрузки изображения")
                    return

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data='Category')],
            [InlineKeyboardButton(text='Прошлая пицца', callback_data=f'back_pizza_{index}')] if index > 0 else [],
            [InlineKeyboardButton(text='Следующая пицца', callback_data=f'next_pizza_{index}')],
            [InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_to_cart_{product['id']}')],
            [InlineKeyboardButton(text='Просмотреть корзину', callback_data='show_cart')],
            [InlineKeyboardButton(text='Почистить корзину', callback_data='clear_cart')]
        ])
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=BufferedInputFile(image_bytes, filename="product.jpg"),
                caption=f"🛒 {product['name']}\n💰 Цена: {product['price']}$ \nСостав:{product['description']}"
            ),
            reply_markup=keyboard
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
    show=await show_cart(user_id)
    print(succes)
    print(show)

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