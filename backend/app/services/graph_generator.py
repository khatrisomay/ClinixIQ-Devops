import io

import matplotlib

matplotlib.use("Agg")  # Non-interactive headless backend
import matplotlib.pyplot as plt
import numpy as np

# Dark Theme styling variables matching ClinixIQ frontend
BG_COLOR = "#0f172a"  # slate-900
AXIS_COLOR = "#334155"  # slate-700
TEXT_COLOR = "#94a3b8"  # slate-400
TITLE_COLOR = "#f8fafc"  # slate-50
PATIENT_COLOR = "#38bdf8"  # sky-400
BASELINE_COLOR = "#10b981"  # emerald-500
ALERT_COLOR = "#f43f5e"  # rose-500


def generate_risk_curve_svg(condition_name: str = "Viral URI", peak_day: int = 4) -> str:
    """
    Generates a high-resolution vector SVG plot showing the patient's
    14-day symptom severity trajectory against the demographic baseline.
    """
    days = np.linspace(1, 14, 100)

    # Mathematical model for acute viral/illness trajectory
    # Gamma/skewed bell curve centered near peak_day
    patient_curve = 85.0 * np.exp(-0.5 * ((days - peak_day) / 2.2) ** 2) + 12.0
    patient_curve = np.clip(patient_curve, 8, 98)

    # Demographic reference population baseline (low stable risk)
    demographic_baseline = 15.0 + 3.0 * np.sin(days / 2.0)

    fig, ax = plt.subplots(figsize=(8, 3.2), dpi=100)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    # Plot lines
    ax.plot(
        days,
        patient_curve,
        color=PATIENT_COLOR,
        linewidth=2.8,
        label="Patient Symptom Severity",
        zorder=3,
    )
    ax.plot(
        days,
        demographic_baseline,
        color=BASELINE_COLOR,
        linewidth=1.8,
        linestyle="--",
        label="Demographic Normal Baseline",
        zorder=2,
    )

    # Fill under patient curve
    ax.fill_between(days, patient_curve, demographic_baseline, color=PATIENT_COLOR, alpha=0.15)

    # Highlight Peak Acuity Point
    peak_idx = int(np.argmax(patient_curve))
    peak_val = patient_curve[peak_idx]
    ax.scatter(
        [days[peak_idx]], [peak_val], color=ALERT_COLOR, s=70, zorder=5, label="Peak Acuity Index"
    )

    # Styling Axes and Spines
    ax.set_xlim(1, 14)
    ax.set_ylim(0, 105)
    ax.set_xlabel("Symptom Timeline (Days)", color=TEXT_COLOR, fontsize=9, fontweight="medium")
    ax.set_ylabel("Severity Index (%)", color=TEXT_COLOR, fontsize=9, fontweight="medium")
    ax.set_title(
        f"Clinical Risk Trajectory & Population Variance • {condition_name}",
        color=TITLE_COLOR,
        fontsize=11,
        fontweight="bold",
        pad=12,
    )

    ax.tick_params(colors=TEXT_COLOR, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(AXIS_COLOR)

    ax.grid(True, linestyle=":", color=AXIS_COLOR, alpha=0.6)

    # Legend
    legend = ax.legend(
        loc="upper right", frameon=True, facecolor="#1e293b", edgecolor=AXIS_COLOR, fontsize=8
    )
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    plt.tight_layout()

    # Save to SVG buffer
    buffer = io.StringIO()
    fig.savefig(
        buffer, format="svg", bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none"
    )
    plt.close(fig)

    return buffer.getvalue()


def generate_differential_bar_svg(differentials_data=None) -> str:
    """
    Generates an SVG horizontal bar chart for differential diagnosis distribution.
    """
    if not differentials_data:
        conditions = [
            "Viral Bronchitis",
            "Influenza Type A",
            "Allergic Rhinitis",
            "Bacterial Pneumonia",
        ]
        probs = [88, 64, 31, 14]
    else:
        conditions = [d["condition"] for d in differentials_data]
        probs = [d["probability"] for d in differentials_data]

    # Invert for top-down display
    conditions = conditions[::-1]
    probs = probs[::-1]

    fig, ax = plt.subplots(figsize=(6.5, 3.0), dpi=100)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    colors = [
        ALERT_COLOR if p > 75 else (PATIENT_COLOR if p > 40 else BASELINE_COLOR) for p in probs
    ]
    bars = ax.barh(conditions, probs, color=colors, height=0.55, edgecolor="none", zorder=3)

    # Annotate probability values
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 2,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)}%",
            va="center",
            ha="left",
            color=TITLE_COLOR,
            fontsize=8,
            fontweight="bold",
        )

    ax.set_xlim(0, 105)
    ax.set_xlabel("Probability Match (%)", color=TEXT_COLOR, fontsize=9)
    ax.set_title(
        "Differential Diagnosis Probability Spectrum",
        color=TITLE_COLOR,
        fontsize=10,
        fontweight="bold",
    )

    ax.tick_params(colors=TEXT_COLOR, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(AXIS_COLOR)

    ax.grid(True, axis="x", linestyle=":", color=AXIS_COLOR, alpha=0.6)
    plt.tight_layout()

    buffer = io.StringIO()
    fig.savefig(
        buffer, format="svg", bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none"
    )
    plt.close(fig)

    return buffer.getvalue()
