import asyncio
import logging.config

import aiohttp
import requests
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from app.config.settings import settings
from app.dto.linkedin_search_params_dto import LinkedInSearchParamsDto


def get_linkedin_member_ids_sync(params: LinkedInSearchParamsDto) -> list[str]:
    """Search LinkedIn members from talent pool service"""
    logging.info(
        f"start get_linkedin_member_ids_sync params: {params.get_talent_pool_query_dict()}"
    )
    api_url = f"{settings.TALENT_POOL_URL}/search/filter"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.TALENT_POOL_TOKEN}",
    }
    response = requests.post(
        api_url,
        headers=headers,
        json=params.get_talent_pool_query_dict(),
    )
    if response.status_code == 200:
        logging.info(f"get response success: {response.json()}")

        response_json = response.json()

        # translate list[int] to list[str]
        return [str(member_id) for member_id in response_json]
    else:
        logging.error(f"get response failed: {response.status_code}, {response.text}")
        raise Exception(
            f"Failed to fetch data: {response.status_code}, {response.text}"
        )


def get_linkedin_member_details_sync(member_id: str) -> dict:
    url = f"{settings.TALENT_POOL_URL}/collect/{member_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.TALENT_POOL_TOKEN}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        # throw error
        raise Exception(f"Error: {response.status_code}, {response.text}")


async def get_linkedin_member_ids(params: LinkedInSearchParamsDto) -> list[str]:
    """Search LinkedIn members"""
    api_url = f"{settings.TALENT_POOL_URL}/search/filter"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.TALENT_POOL_TOKEN}",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            api_url, headers=headers, json=params.dict()
        ) as response:
            if response.status == 200:
                response_json = await response.json()
                return [str(member_id) for member_id in response_json]
            else:
                raise Exception("Failed to fetch data")


async def get_linkedin_member_details_async(
    member_id: str, session: aiohttp.ClientSession
) -> dict:
    url = f"{settings.TALENT_POOL_URL}/collect/{member_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.TALENT_POOL_TOKEN}",
    }

    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            raise Exception(f"Error: {response.status}, {response.text}")
