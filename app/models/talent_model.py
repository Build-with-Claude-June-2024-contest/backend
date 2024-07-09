import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship

from app.config.database import DBBase


class Talent(DBBase):
    __tablename__ = "talents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    core_signal_id = Column(String)
    name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    title = Column(String)
    url = Column(String)
    hash = Column(String)
    location = Column(String)
    industry = Column(String)
    summary = Column(String)
    connections = Column(String)
    recommendations_count = Column(String)
    logo_url = Column(String)
    last_response_code = Column(Integer)
    created = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime)
    outdated = Column(Integer)
    deleted = Column(Integer)
    country = Column(String)
    connections_count = Column(Integer)
    experience_count = Column(Integer)
    last_updated_ux = Column(Integer)
    member_shorthand_name = Column(String)
    member_shorthand_name_hash = Column(String)
    canonical_url = Column(String)
    canonical_hash = Column(String)
    canonical_shorthand_name = Column(String)
    canonical_shorthand_name_hash = Column(String)
    # json fields
    member_also_viewed_collection = Column(JSONB)
    member_awards_collection = Column(JSONB)
    member_certifications_collection = Column(JSONB)
    member_courses_collection = Column(JSONB)
    member_courses_suggestion_collection = Column(JSONB)
    member_education_collection = Column(JSONB)
    member_experience_collection = Column(JSONB)
    member_groups_collection = Column(JSONB)
    member_interests_collection = Column(JSONB)
    member_languages_collection = Column(JSONB)
    member_organizations_collection = Column(JSONB)
    member_patents_collection = Column(JSONB)
    member_posts_see_more_urls_collection = Column(JSONB)
    member_projects_collection = Column(JSONB)
    member_publications_collection = Column(JSONB)
    member_recommendations_collection = Column(JSONB)
    member_similar_profiles_collection = Column(JSONB)
    member_skills_collection = Column(JSONB)
    member_test_scores_collection = Column(JSONB)
    member_volunteering_cares_collection = Column(JSONB)
    member_volunteering_opportunities_collection = Column(JSONB)
    member_volunteering_positions_collection = Column(JSONB)
    member_volunteering_supports_collection = Column(JSONB)
    member_websites_collection = Column(JSONB)
    #
    created_at = Column(DateTime, default=datetime.utcnow)

