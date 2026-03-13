from pydantic import BaseModel

class ChannelPlan(BaseModel):
    channel: str
    objective: str
    tactics: list[str]
    kpis: list[str]
    budget_pct: float

class MarketingStrategy(BaseModel):
    positioning: str
    value_proposition: str
    channel_plans: list[ChannelPlan] = []
    timeline_weeks: int = 8
    total_budget_recommendation: float = 0.0
