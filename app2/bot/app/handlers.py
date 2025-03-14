from aiogram import Router,F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer('Hello', reply_markup=kb.menu)

@router.callback_query(F.data=='Category')
async def catalog(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Select product category', reply_markup=await kb.categories())