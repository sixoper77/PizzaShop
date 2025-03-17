import aiohttp
import asyncio
async def get_data(category_slug=None):
    if category_slug:
        url=f'http://127.0.0.1:8000/api/get-products/{category_slug}'
    else:
        url='http://127.0.0.1:8000/api/get-products/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data=await resp.json()
    return data
async def get_categories():
    url='http://127.0.0.1:8000/api/get_categories'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data=await resp.json()
    return data
async def add_to_cart(cart):
    url='http://127.0.0.1:8000/api/add-to-cart/'
    async with aiohttp.ClientSession() as session:
        async with session.post(url,json=cart) as resp:
            answer=await resp.json()
    return answer

async def clear_cart():
    url='http://127.0.0.1:8000/api/clear-cart/'
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as resp:
            return await resp.json()
    
async def show_cart():
    url='http://127.0.0.1:8000/api/show-cart/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()
        
async def save_telegram_id(telegram_id,username):
    url='http://127.0.0.1:8000/api/save-telegram-id/'
    async with aiohttp.ClientSession() as session:
        async with session.post(url,json={'telegram_id':telegram_id,'username':username}) as resp:
            return await resp.json()        

