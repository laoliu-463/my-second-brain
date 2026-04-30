import csv
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "creator_contents_cleaned.csv"
VIDEO_DIR = ROOT / "raw" / "assets" / "Akkkk缺失视频"
MANIFEST = ROOT / "raw" / "sources" / "Akkkk缺失视频清单.csv"


def is_blank(value: str | None) -> bool:
    return value is None or not value.strip()


def load_missing() -> list[dict[str, str]]:
    with SOURCE_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return [row for row in rows if is_blank(row.get("content_text"))]


def download(row: dict[str, str], target: Path) -> tuple[str, str]:
    if target.exists() and target.stat().st_size > 1024 * 1024:
        return "exists", ""

    url = row.get("video_download_url", "")
    if not url:
        return "missing_url", ""

    tmp = target.with_suffix(".part")
    if tmp.exists():
        tmp.unlink()

    cmd = [
        "curl.exe",
        "-L",
        "--retry",
        "3",
        "--retry-delay",
        "2",
        "--connect-timeout",
        "30",
        "--max-time",
        "600",
        "-A",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
        "-e",
        "https://www.douyin.com/",
        "-o",
        str(tmp),
        url,
    ]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if proc.returncode != 0:
        if tmp.exists():
            tmp.unlink()
        return "failed", (proc.stderr or proc.stdout)[-500:]

    if not tmp.exists() or tmp.stat().st_size < 1024:
        if tmp.exists():
            tmp.unlink()
        return "empty", "downloaded file too small"

    tmp.replace(target)
    return "downloaded", ""


def main() -> int:
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)

    missing = load_missing()
    out_rows: list[dict[str, str]] = []

    for idx, row in enumerate(missing, 1):
        aweme_id = row["aweme_id"]
        target = VIDEO_DIR / f"{row['create_date']}_{aweme_id}.mp4"
        print(f"[{idx}/{len(missing)}] {aweme_id} -> {target.name}", flush=True)
        status, error = download(row, target)
        size = target.stat().st_size if target.exists() else 0
        out_rows.append(
            {
                "aweme_id": aweme_id,
                "create_datetime": row.get("create_datetime", ""),
                "create_date": row.get("create_date", ""),
                "aweme_url": row.get("aweme_url", ""),
                "video_file": str(target.relative_to(ROOT)).replace("\\", "/") if target.exists() else "",
                "download_status": status,
                "file_size_bytes": str(size),
                "engagement_total": row.get("engagement_total", ""),
                "liked_count": row.get("liked_count", ""),
                "collected_count": row.get("collected_count", ""),
                "comment_count": row.get("comment_count", ""),
                "share_count": row.get("share_count", ""),
                "error": error,
            }
        )

    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)

    ok = sum(1 for r in out_rows if r["download_status"] in {"downloaded", "exists"})
    print(f"done: {ok}/{len(out_rows)} available")
    print(MANIFEST)
    return 0 if ok == len(out_rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
