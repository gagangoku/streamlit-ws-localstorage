import asyncio
import ssl

import certifi
import websockets


def main():
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(certifi.where())

    async def query(future):
        async with websockets.connect("wss://linode.liquidco.in/?uid=21", ssl=ssl_context) as ws:
            await ws.send('{"cmd":"echo","msg":"hi4"}')
            response = await ws.recv()
            print ('response: ', response)
            future.set_result(response)

    future1 = asyncio.Future()
    asyncio.run(query(future1))
    print ('future1.result: ', future1.result())


main()
