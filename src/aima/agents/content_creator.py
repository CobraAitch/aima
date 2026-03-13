from click import prompt
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

from aima.agents.campaign_planner import SYSTEM_PROMPT
from aima.agents.state import CampaignState
from aima.llm.factory import create_llm
from aima.models.content import GeneratedContent

SYSTEM_PROMPT = """You are a creative content specialist.
Based on the campaign brief, research, and strategy, generate ready-to-publish
marketing content including social media posts, ad copy, and email subject lines.
Make content platform-specific and aligned with the brand voice.
Keep posts concise and engaging."""

def create_content(state: CampaignState) -> dict:
    """Content creator agent node.

    Generates platform-specific marketing content based on
    the research, strategy, and campaign plan.
    """
    llm = create_llm(temperature=0.8)
    structured_llm = llm.with_structured_output(GeneratedContent)

    brief = state.brief
    prompt = (
        f"Product: {brief.product}\n"
        f"Goal: {brief.goal}\n"
        f"Market: {brief.market}\n\n"
    )

    if state.research:
        prompt += f"Research:\n{state.research[:500]}\n\n"
    if state.strategy:
        prompt += f"Strategy: {state.strategy[:500]}\n\n"

    prompt += (
        "Generate:\n"
        "- 3 social media posts (Instagram, LinkedIn, Twitter)\n"
        "- 2 ad copies\n"
        "- 5 email subject lines\n"
        "- 5 key talking points"
    )

    content = structured_llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])

    return {
        "content": [post.text for post in content.social_media_posts],
        "status": "content_created",
        "messages": [AIMessage(
            content=f"Content created: {len(content.social_media_posts)} posts, "
                    f"{len(content.ad_copies)} ads, "
                    f"{len(content.email_subject_lines)} email subjects"
        )]
    }
