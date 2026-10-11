import streamlit as st
import numpy as np

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

def plot_confusion_matrix(tp: int, fp: int, fn: int, tn: int, title: str = "Model Confusion Matrix"):
    """Plots a 2x2 confusion matrix heatmap perfectly blended with the dark theme."""
    if not MATPLOTLIB_AVAILABLE:
        st.warning("⚠️ Visualization engine initializing...")
        return None

    cm = np.array([[tn, fp], [fn, tp]])
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0b0f19')

    # Custom sleek palette
    cmap = sns.dark_palette("#38bdf8", as_cmap=True)

    sns.heatmap(
        cm, annot=True, fmt="d", cmap=cmap,
        xticklabels=["Predicted Neg", "Predicted Pos"],
        yticklabels=["Actual Neg", "Actual Pos"],
        ax=ax,
        cbar=False,
        annot_kws={"size": 13, "weight": "bold", "color": "#f8fafc"}
    )
    ax.set_xlabel("Predicted Class", color="#94a3b8", fontsize=10, fontweight="bold", labelpad=8)
    ax.set_ylabel("Ground Truth Class", color="#94a3b8", fontsize=10, fontweight="bold", labelpad=8)
    ax.set_title(title, color="#38bdf8", fontsize=12, fontweight="bold", pad=14)
    ax.tick_params(colors="#cbd5e1", labelsize=9)

    for spine in ax.spines.values():
        spine.set_color('#334155')
        spine.set_linewidth(1)

    plt.tight_layout()
    return fig

def plot_metric_bar_chart(metrics: dict, title: str = "Evaluation Performance Metrics"):
    """Plots clean bar chart of evaluation metrics with vibrant gradient accents."""
    if not MATPLOTLIB_AVAILABLE:
        st.warning("⚠️ Visualization engine initializing...")
        return None

    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0b0f19')

    names = list(metrics.keys())
    values = [v * 100 if v <= 1.0 else v for v in metrics.values()]

    colors = ["#38bdf8", "#818cf8", "#34d399", "#c084fc", "#f43f5e"][:len(names)]
    bars = ax.bar(names, values, color=colors, width=0.52, edgecolor="#475569", linewidth=1)
    
    ax.set_ylim(0, 115)
    ax.set_ylabel("Score (%)", color="#94a3b8", fontsize=9, fontweight="bold")
    ax.set_title(title, color="#38bdf8", fontsize=12, fontweight="bold", pad=14)
    ax.tick_params(colors="#cbd5e1", labelsize=9)
    ax.grid(axis='y', linestyle='--', alpha=0.15, color='#94a3b8')

    for spine in ax.spines.values():
        spine.set_color('#334155')

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    color='#f8fafc', fontweight='bold', fontsize=9.5)

    plt.tight_layout()
    return fig
