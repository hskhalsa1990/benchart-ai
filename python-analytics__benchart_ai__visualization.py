from __future__ import annotations
from pathlib import Path
import pandas as pd


def save_benchmark_chart(frame: pd.DataFrame, output: str = "benchmark-chart.png") -> str:
    """Save a grouped benchmark chart. Matplotlib is imported only when called."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    summary = frame.groupby(["name", "group"], as_index=False)["value"].mean()
    pivot = summary.pivot(index="name", columns="group", values="value")
    ax = pivot.plot(kind="bar", figsize=(11, 6), rot=35)
    ax.set_title("Benchart – benchmark comparison")
    ax.set_xlabel("Benchmark")
    ax.set_ylabel("Measured value")
    ax.grid(axis="y", alpha=.25)
    plt.tight_layout()
    path = str(Path(output))
    plt.savefig(path, dpi=160)
    plt.close()
    return path
