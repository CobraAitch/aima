from pydantic import BaseModel

class AudienceSegment(BaseModel):
    name: str
    age_range: str
    interests: list[str]
    platforms: list[str]

class ChannelStrategy(BaseModel):
    channel: str
    objective: str
    budget_pct: float
    key_actions: list[str]

class CampaignBrief(BaseModel):
    product: str
    goal: str
    market: str = "global"
    budget: float | None = None

class CampaignPlan(BaseModel):
    campaign_name: str
    summary: str
    audience_segments: list[AudienceSegment]
    channels: list[ChannelStrategy]
    key_messages: list[str]
    timeline_weeks: int