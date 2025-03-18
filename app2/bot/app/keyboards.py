from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .data import get_data,get_categories
from aiogram.fsm.context import FSMContext
menu=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Категории',callback_data='Category')],
    [InlineKeyboardButton(text='Продукты',callback_data='Products')]
])

async def categories():
    all_categories= await get_categories()
    keyboard=InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.row(InlineKeyboardButton(text=f"{category['name']}",callback_data=f"category_{category['slug']}"))
    keyboard.row(InlineKeyboardButton(text='На главную',callback_data='start'))

    return keyboard.as_markup()

async def products():
    all_products = await get_data()
    keyboard = InlineKeyboardBuilder()

    for product in all_products:
        keyboard.row(InlineKeyboardButton(text=product['name'], callback_data=f"product_{product['id']}"))

    keyboard.row(InlineKeyboardButton(text='На главную', callback_data='start'))
    # keyboard.row(InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_to_cart{product['id']}'))
    

    return keyboard.as_markup()

async def get_items_by_category_slug(category_slug,state:FSMContext):
    products_by_categories=await get_data(category_slug)
    await state.update_data(products=products_by_categories)
    keyboard=InlineKeyboardBuilder()
    for index,item in enumerate(products_by_categories):
        keyboard.row(InlineKeyboardButton(text=item['name'],callback_data=f'product_{item['id']}'))
    keyboard.row(InlineKeyboardButton(text='К категориям ',callback_data='Category'))
    # keyboard.row(InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_to_cart_{item['id']}'))
    keyboard.row(InlineKeyboardButton(text='Просмотреть корзину', callback_data='show_cart'))
    keyboard.row(InlineKeyboardButton(text='Почистить корзину', callback_data='clear_cart'))
    return keyboard.as_markup()
async def back_to_category():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад к категориям', callback_data='category')]
    ])