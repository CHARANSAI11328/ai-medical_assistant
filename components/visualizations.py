import streamlit as st
import numpy as np

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

def plot_confusion_matrix(tp: int, fp: int, fn: int, tn: int, title: str = "Model Confusion Matrix"):
    """Plots a 2x2 confusion matrix heatmap."""
    if not MATPLOTLIB_AVAILABLE:
        st.warning("⚠️ Matplotlib/Seaborn packages are currently initializing.")
        return None

    cm = np.array([[tn, fp], [fn, tp]])
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor('#1e293b')
    ax.set_facecolor('#0f172a')

    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=["Negative", "Positive"],
        yticklabels=["Negative", "Positive"],
        ax=ax,
        cbar=False,
        annot_kws={"size": 12, "weight": "bold", "color": "#f8fafc"}
    )
    ax.set_xlabel("Predicted Label", color="#94a3b8", fontsize=10, fontweight="bold")
    ax.set_ylabel("True Ground Truth", color="#94a3b8", fontsize=10, fontweight="bold")
    ax.set_title(title, color="#38bdf8", fontsize=12, fontweight="bold", pad=12)
    ax.tick_params(colors="#cbd5e1")

    for spine in ax.spines.values():
        spine.set_color('#334155')

    plt.tight_layout()
    return fig

def plot_metric_bar_chart(metrics: dict, title: str = "Evaluation Performance Metrics"):
    """Plots bar chart of evaluation metrics."""
    if not MATPLOTLIB_AVAILABLE:
        st.warning("⚠️ Matplotlib/Seaborn packages are currently initializing.")
        return None

    fig, ax = plt.subplots(figsize=(6, 3.5))
    fig.patch.set_facecolor('#1e293b')
    ax.set_facecolor('#0f172a')

    names = list(metrics.keys())
    values = [v * 100 if v <= 1.0 else v for v in metrics.values()]

    colors = ["#38bdf8", "#818cf8", "#34d399", "#c084fc", "#f43f5e"][:len(names)]
    bars = ax.bar(names, values, color=colors, width=0.55, edgecolor="rgba(255,255,255,0.1)")
    ax.set_ylim(0, 110)
    ax.set_ylabel("Percentage (%)", color="#94a3b8", fontsize=9, fontweight="bold")
    ax.set_title(title, color="#38bdf8", fontsize=12, fontweight="bold", pad=12)
    ax.tick_params(colors="#cbd5e1")

    for spine in ax.spines.values():
        spine.set_color('#334155')

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    color='#f8fafc', fontweight='bold', fontsize=9)

    plt.tight_layout()
    return fig
