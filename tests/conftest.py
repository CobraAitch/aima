import pytest
from unittest.mock import MagicMock

from langchain_core.messages import AIMessage
from aima.models.campaign import CampaignBrief

@pytest.fixture
def sample_brief() -> CampaignBrief:
    return CampaignBrief(
        prdouct="BMW iX",
        goal="Launch social media campaign",
        market="Europe",
        budget=100_000,
    )

@pytest.fixture
def mock_llm() -> MagicMock:
    llm = MagicMock()
    llm.invoke.return_value = AIMessage(content="Mock response")
    return llm
