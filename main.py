from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from for_bot import bot_token, api_redebout
from requests import get, post
import pandas as pd


bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Hello everybody")
    print(execute_query("1258228"))


API_KEY = api_redebout
HEADER = {"x-tonalytica-api-key": API_KEY}

BASE_URL = "https://tonalytica.redoubt.online/api/v1/"


def make_api_url(module, action, ID):
    url = BASE_URL + module + "/" + ID + "/" + action
    return url


def execute_query(query_id):
    """
    Takes in the query ID.tpyt
    Calls the API to execute the query.
    Returns the execution ID of the instance which is executing the query.
    """

    url = make_api_url("query", "execute", query_id)
    print(url)
    response = post(url, headers=HEADER)
    print(response)
    execution_id = response.json()["execution_id"]
    return execution_id


def get_query_status(execution_id):
    """
    Takes in an execution ID.
    Fetches the status of query execution using the API
    Returns the status response object
    """
    url = make_api_url("execution", "status", execution_id)
    response = get(url, headers=HEADER)
    return response


def execute_query_with_params(query_id, param_dict):
    """
    Takes in the query ID. And a dictionary containing parameter values.
    Calls the API to execute the query.
    Returns the execution ID of the instance which is executing the query.
    """

    url = make_api_url("query", "execute", query_id)
    response = post(url, headers=HEADER, json={"query_parameters": param_dict})
    execution_id = response.json()["execution_id"]

    return execution_id


if __name__ == "__main__":
    executor.start_polling(dp)
