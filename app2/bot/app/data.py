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

async def add_to_cart(cart,user_id=None):
    url='http://127.0.0.1:8000/api/add-to-cart/'
    if user_id:
        url+=f'?telegram_id={user_id}'
    async with aiohttp.ClientSession() as session:
        async with session.post(url,json=cart) as resp:
            answer=await resp.json()
    return answer

async def clear_cart(user_id=None):
    url='http://127.0.0.1:8000/api/clear-cart/'
    if user_id:
        url+=f'?telegram_id={user_id}'
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as resp:
            return await resp.json()
    
async def show_cart(user_id=None):
    url='http://127.0.0.1:8000/api/show-cart/'
    if user_id:
        url+=f'?telegram_id={user_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()
        
async def save_telegram_order(order, user_id=None):
    url = 'http://127.0.0.1:8000/api/save-telegram-order/'
    if user_id:
        url += f'?telegram_id={user_id}'
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=order) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    try:
                        error_json = await resp.json()
                        print(f"Ошибка API: {resp.status}. JSON: {error_json}")
                        return {"status": "error", "message": error_json}
                    except:
                        error_text = await resp.text()
                        print(f"Ошибка API: {resp.status}. Ответ: {error_text}")
                        return {"status": "error", "message": f"Ошибка API: {resp.status}"}
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            return {"status": "error", "message": f"Ошибка соединения: {str(e)}"}
        
async def save_telegram_id(telegram_id,username):
    url='http://127.0.0.1:8000/api/save-telegram-id/'
    async with aiohttp.ClientSession() as session:
        async with session.post(url,json={'telegram_id':telegram_id,'username':username}) as resp:
            return await resp.json()    
async def checkout_telegram(order_id):
    url = 'http://127.0.0.1:8000/api/create-checkout-session-telegram'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json={'order_id': order_id}) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    print(f"Ошибка от сервера: {error_text}")
                    return {'error': 'Ошибка при создании платежа'}
        except Exception as e:
            print(f"Ошибка при запросе: {str(e)}")
            return {'error': str(e)}

async def get_image_url(image_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status==200:
                return await response.read()
            else:
                return