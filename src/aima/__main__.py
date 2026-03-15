import logging

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from aima.graph.workflow import build_graph
from aima.models.campaign import CampaignBrief

app = typer.Typer(help="AIMA — AI Marketing Automation")
console = Console()


@app.command()
def run(
    product: str = typer.Option(..., help="Product or brand name"),
    goal: str = typer.Option(..., help="Campaign goal"),
    market: str = typer.Option("global", help="Target market"),
    budget: float | None = typer.Option(None, help="Campaign budget in USD"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
) -> None:
    """Generate a full marketing campaign from a brief."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s  %(message)s",
        datefmt="%H:%M:%S",
    )

    brief = CampaignBrief(product=product, goal=goal, market=market, budget=budget)

    console.print(
        Panel(
            f"[bold]{brief.product}[/bold]\n"
            f"Goal: {brief.goal}\n"
            f"Market: {brief.market}\n"
            f"Budget: {brief.format_budget()}",
            title="Campaign Brief",
        )
    )

    with console.status("[bold green]Running agents..."):
        graph = build_graph()
        try:
            result = graph.invoke({"messages": [], "brief": brief})
        except Exception as exc:
            console.print(f"[bold red]Workflow failed:[/bold red] {exc}")
            raise typer.Exit(code=1) from exc

    plan = result.get("plan")
    if plan:
        table = Table(title="Campaign Plan")
        table.add_column("Field", style="cyan")
        table.add_column("Value")
        table.add_row("Campaign", plan.campaign_name)
        table.add_row("Summary", plan.summary)
        table.add_row("Audience", f"{len(plan.audience_segments)} segments")
        table.add_row("Channels", f"{len(plan.channels)} channels")
        table.add_row("Timeline", f"{plan.timeline_weeks} weeks")
        console.print(table)

    content = result.get("content")
    if content and content.social_media_posts:
        console.print("\n[bold]Generated Content[/bold]")
        for i, post in enumerate(content.social_media_posts, 1):
            console.print(f"  [{i}] [dim]{post.platform}[/dim] {post.text[:120]}")

    console.print("\n[bold]Agent Log[/bold]")
    for msg in result.get("messages", []):
        console.print(f"  -> {msg.content}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
