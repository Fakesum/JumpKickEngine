def get_proxies()->list[str]:
    import asyncio
    from proxybroker import Broker

    res = []

    async def return_val(proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None: break
            res.append(proxy)

    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTP', 'HTTPS'], limit=10),
        return_val(proxies))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

    return res