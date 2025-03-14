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
