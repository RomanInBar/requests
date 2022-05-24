import asyncio
import re
import time
from typing import Any, Dict

import aiohttp


async def request(link: str) -> Any:
    '''Async requests for link'''
    async with aiohttp.ClientSession() as session:
        try:
            async with await session.get(f'https://{link}') as response:
                return response.status
        except aiohttp.ClientConnectionError:
            return 'Error'


async def main() -> None:
    tasks = []
    data: Dict[str, int] = {}
    link = input('Link: https://')
    count = int(input('Count requests: '))
    tasks = [asyncio.create_task(request(link)) for _ in range(count)]
    await asyncio.gather(*tasks)
    for status in tasks:
        result = ''.join(re.findall(r'result=\S+[^ <,> ]', str(status)))
        if result in data:
            data[result] += 1
        else:
            data[result] = 1
    print()
    print(f'Address: {link}.\nResponse: {data}')


start = time.monotonic()
asyncio.run(main())
print(f'Time of work: {time.monotonic() - start:.3f}')
