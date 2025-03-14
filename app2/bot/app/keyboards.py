from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .data import get_data,get_categories
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
    all_products= await get_data()
    keyboard=InlineKeyboardBuilder()
    for product in all_products:
        keyboard.row(InlineKeyboardButton(text=product['name'],callback_data=f'product_{product['id']}'))
    keyboard.row(InlineKeyboardButton(text='На главную',callback_data='start'))
    return keyboard.as_markup()

async def get_items_by_category_slug(category_slug):
    products_by_categories=await get_data(category_slug)
    keyboard=InlineKeyboardBuilder()
    for item in products_by_categories:
        print(item)
        keyboard.row(InlineKeyboardButton(text=item['name'],callback_data=f'product_{item['name']}'))
    keyboard.row(InlineKeyboardButton(text='К категориям ',callback_data='category'))
    return keyboard.as_markup()
async def back_to_category():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад к категориям', callback_data='category')]
    ])
    