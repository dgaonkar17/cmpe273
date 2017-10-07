import requests
import asyncio

def http_call_sync():
    r = requests.get('https://httpbin.org/status/200')
    print(r.status_code)

    r = requests.get('https://httpbin.org/status/204')
    print(r.status_code)

async def http_get(website):
    res = requests.get(website)
    return res
    
    
async def getAsysnc(website, fuId=None):
    print("Waiting "+str(fuId))
    res = await http_get(website)
    print(res.status_code)

loop = asyncio.get_event_loop()
task1 = asyncio.ensure_future(getAsysnc('https://httpbin.org/status/200', 1))
task2 = asyncio.ensure_future(getAsysnc('https://httpbin.org/status/204', 2))

tasks = asyncio.gather(task1, task2)
loop.run_until_complete(tasks)
loop.close()

http_call_sync()

