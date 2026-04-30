import csv
from pathlib import Path

import cv2


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "raw" / "sources" / "Akkkk缺失视频清单.csv"
OUT = ROOT / "raw" / "sources" / "Akkkk缺失视频媒体信息.csv"


def probe_video(path: Path) -> dict[str, str]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        return {
            "probe_status": "failed",
            "width": "",
            "height": "",
            "fps": "",
            "frame_count": "",
            "duration_seconds": "",
        }

    fps = cap.get(cv2.CAP_PROP_FPS) or 0
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    cap.release()
    duration = frames / fps if fps else 0
    return {
        "probe_status": "ok",
        "width": str(width),
        "height": str(height),
        "fps": f"{fps:.3f}",
        "frame_count": str(int(frames)),
        "duration_seconds": f"{duration:.3f}",
    }


def main() -> int:
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    out_rows: list[dict[str, str]] = []
    for row in rows:
        video_file = row.get("video_file", "")
        path = ROOT / video_file if video_file else None
        meta = (
            probe_video(path)
            if path and path.exists()
            else {
                "probe_status": "missing_file",
                "width": "",
                "height": "",
                "fps": "",
                "frame_count": "",
                "duration_seconds": "",
            }
        )
        out_rows.append({**row, **meta})

    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)

    ok = sum(1 for row in out_rows if row["probe_status"] == "ok")
    total_duration = sum(float(row["duration_seconds"] or 0) for row in out_rows)
    print(f"probed={ok}/{len(out_rows)} total_duration_seconds={total_duration:.1f}")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
