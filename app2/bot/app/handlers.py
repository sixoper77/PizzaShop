from aiogram import Router,F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import app.keyboards as kb
from aiogram.fsm.context import FSMContext 
router = Router()
from io import BytesIO
import aiohttp
from aiogram import Router
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer('Hello', reply_markup=kb.menu)

@router.callback_query(F.data=='Category')
async def catalog(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Select product category', reply_markup=await kb.categories())
    
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
    product_name = callback.data.replace('product_', '')
    product = next((p for p in products if p["name"] == product_name), None)
    
    image_url = product.get("image_url")  # URL изображения

    # Загружаем картинку через aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                image_bytes = await response.read()
            else:
                await callback.message.answer("Ошибка загрузки изображения")
                return

    # Отправляем фото через BufferedInputFile
    await callback.message.answer_photo(
        photo=BufferedInputFile(image_bytes, filename="product.jpg"),
        caption=f"🛒 {product['name']}\n💰 Цена: {product['price']} грн"
    )