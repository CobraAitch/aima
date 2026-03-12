from typing import Annotated

from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from pydantic import BaseModel

from aima.models.campaign import CampaignBrief, CampaignPlan

class CampaignState(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages]
    brief: CampaignBrief
    research: str = ""
    plan: CampaignPlan | None = None
    content: list[str] = []
    status: str = "pending"