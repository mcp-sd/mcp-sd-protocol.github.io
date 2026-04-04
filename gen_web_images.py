#!/usr/bin/env python3
"""Generate images for the S2SP protocol website."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__)) + "/images"
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "figure.facecolor": "#0d1117",
    "axes.facecolor": "#0d1117",
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.3,
})

# Colors
BG = "#0d1117"
CARD = "#161b22"
BLUE = "#58a6ff"
GREEN = "#3fb950"
ORANGE = "#d29922"
RED = "#f85149"
PURPLE = "#bc8cff"
WHITE = "#e6edf3"
GRAY = "#8b949e"
BORDER = "#30363d"


def draw_box(ax, x, y, w, h, label, color, sublabel=None):
    box = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.15",
                         facecolor=CARD, edgecolor=color, linewidth=2.5)
    ax.add_patch(box)
    if sublabel:
        ax.text(x, y+0.15, label, ha="center", va="center", fontsize=13,
                fontweight="bold", color=color)
        ax.text(x, y-0.2, sublabel, ha="center", va="center", fontsize=9, color=GRAY)
    else:
        ax.text(x, y, label, ha="center", va="center", fontsize=13,
                fontweight="bold", color=color)


def draw_arrow(ax, x1, y1, x2, y2, color, lw=2, ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls, mutation_scale=15))


# ========== Hero diagram: Traditional vs S2SP ==========
def hero_diagram():
    fig, ax = plt.subplots(figsize=(16, 7))
    ax.set_xlim(-1, 17)
    ax.set_ylim(-3, 4)
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # ── Left: Traditional MCP ──
    ax.text(4, 3.2, "Without S2SP", ha="center", fontsize=14, color=RED, fontweight="bold")

    draw_box(ax, 1.2, 1.5, 2.0, 1.0, "Weather\nServer", GREEN)
    draw_box(ax, 4.0, 1.5, 2.0, 1.0, "Agent", BLUE, "LLM")
    draw_box(ax, 6.8, 1.5, 2.0, 1.0, "Stats\nServer", ORANGE)

    # All 30 columns flow through agent
    draw_arrow(ax, 2.3, 1.5, 2.9, 1.5, RED, lw=3)
    draw_arrow(ax, 5.1, 1.5, 5.7, 1.5, RED, lw=3)

    ax.text(4, 0.3, "All 30 columns flow through agent", ha="center", fontsize=10, color=RED)
    ax.text(4, -0.2, "~10,000 tokens consumed", ha="center", fontsize=9, color=GRAY)

    # ── Divider ──
    ax.plot([8.2, 8.2], [-2.5, 3.5], color=BORDER, lw=1.5, ls="--")
    ax.text(8.2, 3.5, "vs", ha="center", fontsize=12, color=GRAY,
            bbox=dict(boxstyle="round,pad=0.2", facecolor=BG, edgecolor="none"))

    # ── Right: S2SP ──
    ax.text(12.8, 3.2, "With S2SP", ha="center", fontsize=14, color=GREEN, fontweight="bold")

    draw_box(ax, 10, 0.0, 2.2, 1.0, "Weather\nServer", GREEN)
    draw_box(ax, 12.8, 2.2, 2.2, 1.0, "Agent", BLUE, "LLM")
    draw_box(ax, 15.5, 0.0, 2.2, 1.0, "Stats\nServer", ORANGE)

    # Control plane: Weather -> Agent (abstract only)
    draw_arrow(ax, 10.8, 0.55, 11.9, 1.7, BLUE, lw=2, ls="--")
    ax.text(10.6, 1.4, "abstract\ndomains\nonly", ha="center", fontsize=8, color=BLUE,
            style="italic", linespacing=1.2)

    # Control plane: Agent -> Stats (abstract + resource_url)
    draw_arrow(ax, 13.7, 1.7, 14.8, 0.55, BLUE, lw=2, ls="--")
    ax.text(15.0, 1.4, "abstract +\nresource_url", ha="center", fontsize=8, color=BLUE,
            style="italic", linespacing=1.2)

    # Data plane: Stats -> Weather (fetch body)
    draw_arrow(ax, 14.4, -0.1, 11.2, -0.1, GREEN, lw=4)
    ax.text(12.8, -0.7, "POST /s2sp/data/{token}", ha="center",
            fontsize=9, color=GREEN, fontweight="bold", family="monospace")
    ax.text(12.8, -1.2, "Body domains fetched directly (data plane)", ha="center",
            fontsize=9, color=GRAY)

    # Labels
    ax.text(12.8, -2.0, "Agent sees ~600 tokens  |  Body (~9,000 tokens) never enters agent",
            ha="center", fontsize=10, color=GREEN, fontweight="bold")

    fig.savefig(f"{OUT}/hero_diagram.png", facecolor=BG)
    plt.close()


# ========== How it works (3 steps) ==========
def how_it_works():
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    fig.patch.set_facecolor(BG)

    titles = [
        "1. Agent Gets Abstract",
        "2. Agent Filters & Decides",
        "3. Consumer Fetches Body"
    ]
    colors = [BLUE, PURPLE, GREEN]

    for ax in axes:
        ax.set_xlim(-0.5, 7.5)
        ax.set_ylim(-2.5, 3.5)
        ax.axis("off")
        ax.set_facecolor(BG)

    # Step 1: Agent calls tool with abstract_domains
    ax = axes[0]
    ax.text(3.5, 3.2, titles[0], ha="center", fontsize=13, color=colors[0], fontweight="bold")
    draw_box(ax, 1.5, 1, 2.5, 1.0, "Weather\nServer", GREEN)
    draw_box(ax, 5.5, 1, 2.5, 1.0, "Agent", BLUE)
    draw_arrow(ax, 2.9, 1.3, 4.2, 1.3, BLUE, lw=2.5)
    ax.text(3.5, 1.8, "abstract only", fontsize=9, color=BLUE, ha="center", style="italic")
    ax.text(3.5, -0.5, 'get_alerts(area="CA",', ha="center", fontsize=9,
            color=WHITE, family="monospace")
    ax.text(3.5, -1.1, '  abstract_domains=', ha="center", fontsize=9,
            color=WHITE, family="monospace")
    ax.text(3.5, -1.7, '  "event,severity")', ha="center", fontsize=9,
            color=GREEN, family="monospace")

    # Step 2: Agent filters on abstract
    ax = axes[1]
    ax.text(3.5, 3.2, titles[1], ha="center", fontsize=13, color=colors[1], fontweight="bold")
    draw_box(ax, 3.5, 1.2, 3, 1.5, "Agent", BLUE, "LLM")
    # Show abstract rows
    ax.text(3.5, 0.0, '_row_id  event         severity', ha="center",
            fontsize=8, color=GRAY, family="monospace")
    ax.text(3.5, -0.5, '0        Wind Advisory  Moderate', ha="center",
            fontsize=8, color=GREEN, family="monospace")
    ax.text(3.5, -0.9, '1        Flood Watch    Minor', ha="center",
            fontsize=8, color=GRAY, family="monospace")
    ax.text(3.5, -1.3, '2        High Wind      Severe', ha="center",
            fontsize=8, color=GREEN, family="monospace")
    ax.text(3.5, -2.0, 'Selects _row_id 0, 2 (wind alerts)', ha="center",
            fontsize=9, color=PURPLE, style="italic")

    # Step 3: Consumer fetches body from source
    ax = axes[2]
    ax.text(3.5, 3.2, titles[2], ha="center", fontsize=13, color=colors[2], fontweight="bold")
    draw_box(ax, 1.2, 1, 2.0, 1.0, "Weather", GREEN)
    draw_box(ax, 5.8, 1, 2.0, 1.0, "Stats", ORANGE)
    draw_arrow(ax, 4.7, 0.9, 2.3, 0.9, GREEN, lw=3.5)
    ax.text(3.5, 0.1, "body domains", fontsize=9, color=GREEN, ha="center",
            fontweight="bold")
    ax.text(3.5, -0.5, "POST /s2sp/data/{id}", ha="center", fontsize=9,
            color=GREEN, family="monospace")
    ax.text(3.5, -1.2, "Full data fetched directly.", ha="center",
            fontsize=9, color=GRAY)
    ax.text(3.5, -1.7, "Agent never saw body data.", ha="center",
            fontsize=9, color=GRAY, style="italic")

    fig.savefig(f"{OUT}/how_it_works.png", facecolor=BG)
    plt.close()


# ========== Architecture diagram ==========
def architecture():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(-1, 15)
    ax.set_ylim(-5, 4.5)
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    ax.text(7, 4, "S2SP Architecture", ha="center", fontsize=18, color=WHITE, fontweight="bold")
    ax.text(7, 3.3, "Control Plane (abstract) + Data Plane (body)", ha="center",
            fontsize=11, color=GRAY)

    # Agent
    draw_box(ax, 7, 1.5, 3.5, 1.3, "Agent (LLM)", BLUE, "Control Plane")

    # Source server
    draw_box(ax, 2.5, -1.5, 3.5, 2.0, "Source Server", GREEN, "@s2sp_tool()")

    # Consumer server
    draw_box(ax, 11.5, -1.5, 3.5, 2.0, "Consumer Server", ORANGE, "draw_chart()")

    # Control plane: Source -> Agent (abstract only)
    draw_arrow(ax, 4.0, -0.3, 5.5, 0.9, BLUE, lw=2.5)
    ax.text(3.8, 0.7, "abstract\ndomains\n+ _row_id", fontsize=9, color=BLUE,
            ha="center", style="italic", linespacing=1.2)

    # Control plane: Agent -> Consumer (abstract + resource ref)
    draw_arrow(ax, 8.5, 0.9, 10.0, -0.3, BLUE, lw=2.5)
    ax.text(10.2, 0.7, "abstract\n+ resource_url", fontsize=9, color=BLUE,
            ha="center", style="italic", linespacing=1.2)

    # Data plane: Consumer -> Source (fetch body)
    draw_arrow(ax, 9.7, -2.0, 4.5, -2.0, GREEN, lw=5)
    ax.text(7, -1.5, "Data Plane (HTTP)", ha="center", fontsize=11,
            color=GREEN, fontweight="bold")
    ax.text(7, -2.6, "POST /s2sp/data/{token}", ha="center",
            fontsize=10, color=GREEN, family="monospace")
    ax.text(7, -3.2, "Body domains fetched directly — never enters agent", ha="center",
            fontsize=10, color=GRAY, style="italic")

    # Legend
    ly = -4.2
    ax.plot([2, 3], [ly, ly], color=BLUE, lw=2.5)
    ax.text(3.3, ly, "Control Plane (abstract domains via MCP)", fontsize=10, color=BLUE, va="center")
    ax.plot([8.5, 9.5], [ly, ly], color=GREEN, lw=4)
    ax.text(9.8, ly, "Data Plane (body domains via HTTP)", fontsize=10, color=GREEN, va="center")

    fig.savefig(f"{OUT}/architecture.png", facecolor=BG)
    plt.close()


# ========== Token savings chart ==========
def token_savings():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5.5))
    fig.patch.set_facecolor(BG)
    fig.suptitle("S2SP Token Savings (Weather Alert Demo — 8 alerts, 29 columns)",
                 fontsize=14, color=WHITE, fontweight="bold", y=1.02)

    # ── Left panel: tokens by abstract_domains size ──
    ax1.set_facecolor(BG)

    configs = ["2 cols\nevent,severity", "4 cols\n+urgency,status",
               "6 cols\n+headline,area", "All 29 cols\n(no S2SP)"]
    traditional = [6537, 6537, 6537, 6537]  # all cols always
    s2sp_tokens = [469, 578, 1096, 6537]    # measured

    x = np.arange(len(configs))
    w = 0.35

    bars1 = ax1.bar(x - w/2, traditional, w, label="Traditional MCP",
                    color=RED, alpha=0.85, edgecolor="none")
    bars2 = ax1.bar(x + w/2, s2sp_tokens, w, label="S2SP (abstract only)",
                    color=GREEN, alpha=0.85, edgecolor="none")

    for bar, val in zip(bars1, traditional):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                f"{val:,}", ha="center", fontsize=8, color=RED, fontweight="bold")
    for bar, val in zip(bars2, s2sp_tokens):
        pct = (1 - val / 6537) * 100
        label = f"{val:,}\n({pct:.0f}% saved)" if pct > 0 else f"{val:,}"
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                label, ha="center", fontsize=7, color=GREEN, fontweight="bold")

    ax1.set_ylabel("Tokens in Agent Context", fontsize=11, color=WHITE)
    ax1.set_xticks(x)
    ax1.set_xticklabels(configs, fontsize=8, color=GRAY)
    ax1.legend(fontsize=9, facecolor=CARD, edgecolor=BORDER, labelcolor=WHITE)
    ax1.tick_params(colors=GRAY)
    ax1.spines["bottom"].set_color(BORDER)
    ax1.spines["left"].set_color(BORDER)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.set_title("Tokens by Abstract Domains Size", fontsize=12, color=WHITE, pad=10)

    # ── Right panel: data flow breakdown ──
    ax2.set_facecolor(BG)

    categories = ["Control Plane\n(agent sees)", "Data Plane\n(server-to-server)"]
    sizes_data = [469, 5609]  # 2-col abstract vs body
    colors_data = [BLUE, GREEN]

    bars = ax2.barh(categories, sizes_data, color=colors_data, alpha=0.85, edgecolor="none", height=0.5)
    for bar, val in zip(bars, sizes_data):
        ax2.text(bar.get_width() + 80, bar.get_y() + bar.get_height()/2,
                f"{val:,} tokens", ha="left", va="center", fontsize=11,
                color=WHITE, fontweight="bold")

    ax2.set_xlim(0, max(sizes_data) * 1.4)
    ax2.set_xlabel("Tokens", fontsize=11, color=WHITE)
    ax2.tick_params(colors=GRAY)
    ax2.spines["bottom"].set_color(BORDER)
    ax2.spines["left"].set_color(BORDER)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.set_title("Data Flow: 2-Column Abstract", fontsize=12, color=WHITE, pad=10)

    plt.tight_layout()

    fig.savefig(f"{OUT}/token_savings.png", facecolor=BG)
    plt.close()


if __name__ == "__main__":
    print("Generating website images...")
    hero_diagram()
    print("  hero_diagram.png")
    how_it_works()
    print("  how_it_works.png")
    architecture()
    print("  architecture.png")
    token_savings()
    print("  token_savings.png")
    print("Done!")
