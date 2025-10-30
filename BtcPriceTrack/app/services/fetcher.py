import aiohttp


async def fetch_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if "bitcoin" not in data:
                print("Unexpected response:", data)
                return None
            return data["bitcoin"]["usd"]
