import asyncio

import aiohttp
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.talent_model import Talent
from app.services.talent_pool_service import get_linkedin_member_details_async


async def get_talent_details_by_ids(
    talent_ids: list[str], db_session: Session
) -> list[dict]:
    """
    Get talent details by ids
    """

    talent_details = []
    talent_details_not_in_db = []
    # check the talent data is in the database
    stmt = select(Talent).where(Talent.core_signal_id.in_(talent_ids))
    talent_details_in_db = db_session.execute(stmt).scalars().all()
    talent_ids_in_db = [talent.core_signal_id for talent in talent_details_in_db]
    talent_ids_not_in_db = [
        talent_id for talent_id in talent_ids if talent_id not in talent_ids_in_db
    ]

    # if not, get the talent details from talent pool API
    if talent_ids_not_in_db:
        async with aiohttp.ClientSession() as session:
            tasks = [
                get_linkedin_member_details_async(talent_id, session)
                for talent_id in talent_ids_not_in_db
            ]
            talent_details_json = await asyncio.gather(*tasks)
            for talent_detail_json in talent_details_json:
                talent_details.append(talent_detail_json)
                talent_model = get_talent_model_from_json(
                    talent_detail_json=talent_detail_json
                )
                talent_details_not_in_db.append(talent_model)

    # TODO: batch store talent details not in database to database
    if talent_details_not_in_db:
        db_session.add_all(talent_details_not_in_db)
        db_session.commit()
        # Refresh each instance individually
        for talent_model in talent_details_not_in_db:
            db_session.refresh(talent_model)

    # add talent details in db to talent_details
    talent_details.extend(talent_details_in_db)

    return talent_details


def get_talent_model_from_json(talent_detail_json: dict) -> Talent:
    """
    Store talent details in the database.

    Args:
        talent_details (dict): The talent details to store.
        db_session (Session): The database session.

    Returns:
        Talent: The stored Talent object.
    """
    talent = Talent(
        core_signal_id=str(talent_detail_json.get("id")),
        name=talent_detail_json.get("name"),
        first_name=talent_detail_json.get("first_name"),
        last_name=talent_detail_json.get("last_name"),
        title=talent_detail_json.get("title"),
        url=talent_detail_json.get("url"),
        hash=talent_detail_json.get("hash"),
        location=talent_detail_json.get("location"),
        industry=talent_detail_json.get("industry"),
        summary=talent_detail_json.get("summary"),
        connections=talent_detail_json.get("connections"),
        recommendations_count=talent_detail_json.get("recommendations_count"),
        logo_url=talent_detail_json.get("logo_url"),
        last_response_code=talent_detail_json.get("last_response_code"),
        last_updated=talent_detail_json.get("last_updated"),
        outdated=talent_detail_json.get("outdated"),
        deleted=talent_detail_json.get("deleted"),
        country=talent_detail_json.get("country"),
        connections_count=talent_detail_json.get("connections_count"),
        experience_count=talent_detail_json.get("experience_count"),
        last_updated_ux=talent_detail_json.get("last_updated_ux"),
        member_shorthand_name=talent_detail_json.get("member_shorthand_name"),
        member_shorthand_name_hash=talent_detail_json.get("member_shorthand_name_hash"),
        canonical_url=talent_detail_json.get("canonical_url"),
        canonical_hash=talent_detail_json.get("canonical_hash"),
        canonical_shorthand_name=talent_detail_json.get("canonical_shorthand_name"),
        canonical_shorthand_name_hash=talent_detail_json.get(
            "canonical_shorthand_name_hash"
        ),
        member_also_viewed_collection=talent_detail_json.get(
            "member_also_viewed_collection"
        ),
        member_awards_collection=talent_detail_json.get("member_awards_collection"),
        member_certifications_collection=talent_detail_json.get(
            "member_certifications_collection"
        ),
        member_courses_collection=talent_detail_json.get("member_courses_collection"),
        member_courses_suggestion_collection=talent_detail_json.get(
            "member_courses_suggestion_collection"
        ),
        member_education_collection=talent_detail_json.get(
            "member_education_collection"
        ),
        member_experience_collection=talent_detail_json.get(
            "member_experience_collection"
        ),
        member_groups_collection=talent_detail_json.get("member_groups_collection"),
        member_interests_collection=talent_detail_json.get(
            "member_interests_collection"
        ),
        member_languages_collection=talent_detail_json.get(
            "member_languages_collection"
        ),
        member_organizations_collection=talent_detail_json.get(
            "member_organizations_collection"
        ),
        member_patents_collection=talent_detail_json.get("member_patents_collection"),
        member_posts_see_more_urls_collection=talent_detail_json.get(
            "member_posts_see_more_urls_collection"
        ),
        member_projects_collection=talent_detail_json.get("member_projects_collection"),
        member_publications_collection=talent_detail_json.get(
            "member_publications_collection"
        ),
        member_recommendations_collection=talent_detail_json.get(
            "member_recommendations_collection"
        ),
        member_similar_profiles_collection=talent_detail_json.get(
            "member_similar_profiles_collection"
        ),
        member_skills_collection=talent_detail_json.get("member_skills_collection"),
        member_test_scores_collection=talent_detail_json.get(
            "member_test_scores_collection"
        ),
        member_volunteering_cares_collection=talent_detail_json.get(
            "member_volunteering_cares_collection"
        ),
        member_volunteering_opportunities_collection=talent_detail_json.get(
            "member_volunteering_opportunities_collection"
        ),
        member_volunteering_positions_collection=talent_detail_json.get(
            "member_volunteering_positions_collection"
        ),
        member_volunteering_supports_collection=talent_detail_json.get(
            "member_volunteering_supports_collection"
        ),
        member_websites_collection=talent_detail_json.get("member_websites_collection"),
    )

    return talent
