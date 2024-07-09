import asyncio
import logging.config
import time

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.dto.talent_query_dto import TalentQueryCreateDto
from app.enums.credit_type_enum import CreditTypeEnum
from app.infrastructure.dependencies import get_pageable_param
from app.infrastructure.logger import log_message
from app.infrastructure.schemas import PageableParamDTO
from app.models.talent_model import Talent
from app.models.talent_query_model import TalentQuery
from app.services.talent_pool_service import get_linkedin_member_ids_sync
from app.services.credit_service import consume_credits
from app.services.structure_query_service import natural_language_to_structured_query
from app.services.talent_service import (
    get_talent_details_by_ids,  # Assuming this service exists
)
from app.user import models as user_model
from app.user.services import get_current_user_base_on_config

talent_query_router = APIRouter()


@talent_query_router.post("")
def create_talent_query(
    talent_query_create_dto: TalentQueryCreateDto,
    db_session: Session = Depends(get_db),
    user: user_model.User = Depends(get_current_user_base_on_config),
):
    """Use natural language query to create a talent query.

    Args:
        talent_query_create_dto (TalentQueryCreateDto): The natural language query to create a talent query.
        db_session (Session): The database session.
        user (User): The user who created the talent query.

    Returns:
        dict: The talent query id.
    """
    log_message(
        level="info",
        event="Start create_talent_query",
        user_id=user.id,
        talent_query_create_dto=talent_query_create_dto.model_dump(),
    )

    # get structured query from LLM
    structured_query = natural_language_to_structured_query(
        natural_language_query=talent_query_create_dto.nature_language_query
    )

    log_message(
        level="info",
        event="Structured query generated",
        structured_query=structured_query,
    )

    # save query to database
    # TODO: refactor below to service
    talent_query = TalentQuery(
        nature_language_query=talent_query_create_dto.nature_language_query,
        structured_query=structured_query.get_talent_pool_query_dict(),
        query_result=[],
        user_id=user.id,
    )
    # TODO: count the token used

    db_session.add(talent_query)
    db_session.commit()
    db_session.refresh(talent_query)

    log_message(
        level="info",
        event="Saved talent_query",
        # talent_query=talent_query.model_dump(),
    )

    # use talent pool API to get talent ids
    talent_ids = get_linkedin_member_ids_sync(params=structured_query)
    # save talent ids to database
    talent_query.query_result = talent_ids
    db_session.commit()
    db_session.refresh(talent_query)
    # return talent_query_i
    log_message(
        level="info",
        event="Saved talent_query with results",
        # talent_query=talent_query.model_dump(),
    )
    return {"talent_query_id": talent_query.id}


@talent_query_router.get("/{query_id}")
async def get_talent_details(
    query_id: str,
    page_params: PageableParamDTO = Depends(get_pageable_param),
    db_session: Session = Depends(get_db),
    user: user_model.User = Depends(get_current_user_base_on_config),
):
    """Get the talent details from the talent query.

    Args:
        query_id (str): The talent query id.
        page_params (PageableParamDTO): The page params.
        db_session (Session): The database session.
        user (User): The user who created the talent query.

    Returns:
        dict: The talent details.
    """
    # log the user id
    log_message(
        level="info",
        event="Start get_talent_details",
        user_id=user.id,
        query_id=query_id,
        page_params=page_params.model_dump(),
    )
    # get talent query object from database
    talent_query = (
        db_session.query(TalentQuery).filter(TalentQuery.id == query_id).first()
    )
    if not talent_query:
        raise HTTPException(status_code=404, detail="Talent query not found")

    # get talent ids from talent query object, use the page params to get the talent ids
    talent_ids: list[str] = talent_query.query_result[
        page_params.offset : page_params.offset + page_params.limit
    ]

    # consume credit for the user
    consume_credits(
        user_id=user.id,
        credit_type_name=CreditTypeEnum.CONTACT_CREDIT,
        amount=len(talent_ids),
        db_session=db_session,
    )

    # get talent details from talent pool API
    talent_details = await get_talent_details_by_ids(
        talent_ids=talent_ids, db_session=db_session
    )

    # TODO: use PageableResultDTO
    return {
        "total": len(talent_ids),
        "page": page_params.page,
        "size": page_params.limit,
        "data": talent_details,
    }
