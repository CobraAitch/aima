from aima.graph.workflow import build_graph
from aima.models.campaign import CampaignBrief

def main() -> None:
    app = build_graph()
    brief = CampaignBrief(
        product="BMW iX",
        goal="Launch social media campaign for European market",
        market="Europe",
        budget=100_000,
    )
    result = app.invoke({"messages": [], "brief": brief})

    plan = result["plan"]
    print(f"\n{'='*60}")
    print(f"Campaign:   {plan.campaign_name}")
    print(f"Summary:    {plan.summary}")
    print(f"Audience:   {len(plan.audience_segments)} segments")
    print(f"Channels:   {len(plan.channels)} channels")
    print(f"Timeline:   {plan.timeline_weeks} weeks")
    print(f"{'='*60}\n")

    for msg in result["messages"]:
        print(f"    -> {msg.content}")

    print()

if __name__ == "__main__":
    main()