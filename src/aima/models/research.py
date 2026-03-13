from pydantic import BaseModel

class CompetitorInfo(BaseModel):
    name: str
    strengths: list[str]
    weaknesses: list[str]

class MarketResearch(BaseModel):
    market_overview: str
    target_demographics: list[str] = []
    competitors: list[CompetitorInfo] = []
    trends: list[str] = []
    opportunities: list[str] = []
