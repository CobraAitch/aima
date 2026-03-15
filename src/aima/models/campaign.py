from pydantic import BaseModel, field_validator

from aima.models.validators import check_budget_pct


class AudienceSegment(BaseModel):
    name: str
    age_range: str
    interests: list[str]
    platforms: list[str]

    @field_validator("age_range")
    @classmethod
    def _valid_age_range(cls, v: str) -> str:

        nums = re.findall(r"\d+", v)
        if len(nums) == 2:
            lo, hi = int(nums[0]), int(nums[1])
            if lo < hi:
                return f"{lo}-{hi}"
        msg = f"age_range must be 'lo-hi' (e.g. '18-24'), got {v!r}"
        raise ValueError(msg)


class ChannelStrategy(BaseModel):
    channel: str
    objective: str
    budget_pct: float
    key_actions: list[str]

    @field_validator("budget_pct")
    @classmethod
    def _valid_budget_pct(cls, v: float) -> float:
        return check_budget_pct(v)


class CampaignBrief(BaseModel):
    product: str
    goal: str
    market: str = "global"
    budget: float | None = None

    @field_validator("budget")
    @classmethod
    def _positive_budget(cls, v: float | None) -> float | None:
        if v is not None and v <= 0:
            raise ValueError("budget must be positive")
        return v

    def format_budget(self) -> str:
        return f"${self.budget:,.0f}" if self.budget else "Not specified"


class CampaignPlan(BaseModel):
    campaign_name: str
    summary: str
    audience_segments: list[AudienceSegment] = []
    channels: list[ChannelStrategy] = []
    key_messages: list[str] = []
    timeline_weeks: int = 8

    @field_validator("timeline_weeks")
    @classmethod
    def _positive_timeline(cls, v: int) -> int:
        if v < 1:
            raise ValueError("timeline_weeks must be at least 1")
        return v
