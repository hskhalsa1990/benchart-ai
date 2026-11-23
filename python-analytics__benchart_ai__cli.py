from __future__ import annotations
import argparse, json
from .cleaning import load_benchmark_csv
from .statistics import summarize
from .visualization import save_benchmark_chart
from .ml import detect_anomalies


def main():
    parser = argparse.ArgumentParser(description="Analyze Benchart benchmark CSV data")
    parser.add_argument("csv", help="CSV with name,value and optional group,unit,run columns")
    parser.add_argument("--chart", default=None, help="Save chart to this PNG path")
    parser.add_argument("--anomalies", action="store_true", help="Include anomaly detection")
    args = parser.parse_args()
    frame = load_benchmark_csv(args.csv)
    report = summarize(frame)
    if args.anomalies:
        report["anomalies"] = detect_anomalies(frame).to_dict(orient="records")
    if args.chart:
        report["chart"] = save_benchmark_chart(frame, args.chart)
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
