from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

from aima.config import CampaignStatus
from aima.models.campaign import CampaignBrief, CampaignPlan
from aima.models.content import GeneratedContent
from aima.models.research import MarketResearch
from aima.models.strategy import MarketingStrategy


class CampaignState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
    brief: CampaignBrief
    research: MarketResearch | None
    strategy: MarketingStrategy | None
    plan: CampaignPlan | None
    content: GeneratedContent | None
    status: CampaignStatus
