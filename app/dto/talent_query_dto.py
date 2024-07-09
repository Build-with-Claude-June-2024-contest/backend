from pydantic import BaseModel


class TalentQueryCreateDto(BaseModel):
    """Talent query DTO"""

    nature_language_query: str
