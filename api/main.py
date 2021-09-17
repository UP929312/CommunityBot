from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every ###

from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from endpoints.total import get_total_value
from endpoints.groups import get_groups_value
from endpoints.pages import get_pages_dict
from endpoints.dump import get_dump_dict
from endpoints.debug import get_debug_values
from endpoints.tree import get_tree

from exceptions import InvalidApiKeyException, InvalidUsername, MojangServerError

from data.constants.collector import fetch_prices
#from price_list_updater import update_price_lists

import uvicorn
import aiohttp

limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Data:
    pass

class Session:
    pass

data = Data()
session_object = Session()

@app.on_event("startup")
async def create_session() -> None:
    session_object.session = aiohttp.ClientSession()

@app.on_event("startup")
@repeat_every(seconds=60*60, raise_exceptions=True)  # 1 hour
def update_price_lists_loop() -> None:
    print("Updating price lists loop")

    #data = update_price_lists(data)

    #'''
    data.BAZAAR, data.LOWEST_BIN, data.PRICES = fetch_prices()
    data.BAZAAR["ENDER_PEARL"] = 100
    data.BAZAAR["ENCHANTED_CARROT"] = 1000
    # For overrides
    for item, hard_price in [("RUNE", 5), ("WISHING_COMPASS", 1000), ("PLUMBER_SPONGE", 100), ("ICE_HUNK", 100),]:
        data.LOWEST_BIN[item] = hard_price
    # Price backups
    for item, hard_price in [("SCATHA;2", 250_000_000),("SCATHA;3", 500_000_000), ("SCATHA;4", 1_000_000_000 ), ("GAME_ANNIHILATOR", 2_500_000_000), ("GAME_BREAKER", 1_000_000_000), ]:
        if item not in data.LOWEST_BIN:
            data.LOWEST_BIN[item] = hard_price
    #'''
    

@app.get("/")
@limiter.limit("20/minute")
async def root(request: Request):
    return JSONResponse(status_code=200, content={"message": "Hello world!"})


@app.get("/online")
@limiter.limit("20/minute")
async def test_online(request: Request):
    return JSONResponse(status_code=200, content={"message": "API Operational"})


async def validate(function, params):
    try:
        returned_data = await function(*params)
        if isinstance(returned_data, dict):
            return JSONResponse(status_code=200, content=returned_data)

        print("ERROR!")
        return JSONResponse(status_code=500, content={"message": "An internal exception occured!"})
    except InvalidApiKeyException:
        return JSONResponse(status_code=401, content={"message": "An invalid API key was passed! Please try another key."})
    except InvalidUsername:
        return JSONResponse(status_code=404, content={"message": "Username could not be found!"})
    except MojangServerError:
        return JSONResponse(status_code=503, content={"message": "Mojang's servers didn't respond."})
    except:
        return JSONResponse(status_code=500, content={"message": "An internal exception occured!"})
        
        
@app.get("/pages/{username}")
async def pages(request: Request, username: str, api_key: str):
    return await validate(get_pages_dict, (session_object.session, api_key, data, username))

@app.get("/total/{username}")
async def total(request: Request, username: str, api_key: str):
    return await validate(get_total_value, (session_object.session, api_key, data, username))  


@app.get("/groups/{username}")
async def groups(request: Request, username: str, api_key: str):
    return await validate(get_groups_value, (session_object.session, api_key, data, username))  


@app.get("/dump/{username}")
async def dump(request: Request, username: str, api_key: str):
    return await validate(get_dump_dict, (session_object.session, api_key, data, username))  

@app.get("/debug/{username}")
async def debug(request: Request, username: str, api_key: str):
    return await validate(get_debug_values, (session_object.session, api_key, data, username))


@app.get("/tree/{username}")
async def tree(request: Request, username: str, api_key: str):
    return await validate(get_tree, (session_object.session, api_key, data, username))

if __name__ == "__main__":
    print("Done")
    uvicorn.run(app, host='0.0.0.0', port=8000, debug=True)
