import csv
import json
from pathlib import Path

from faster_whisper import WhisperModel


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "raw" / "sources" / "Akkkk缺失视频媒体信息.csv"
OUT_DIR = ROOT / "raw" / "sources" / "Akkkk缺失视频转写"
SUMMARY = ROOT / "raw" / "sources" / "Akkkk缺失视频转写汇总.csv"


def format_ts(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_m = total_s // 60
    m = total_m % 60
    h = total_m // 60
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def transcribe_one(model: WhisperModel, row: dict[str, str]) -> dict[str, str]:
    aweme_id = row["aweme_id"]
    video_file = row.get("video_file", "")
    if not video_file:
        return {**row, "transcribe_status": "missing_video", "transcript_file": "", "detected_language": "", "segment_count": "0"}

    video_path = ROOT / video_file
    if not video_path.exists():
        return {**row, "transcribe_status": "missing_video", "transcript_file": "", "detected_language": "", "segment_count": "0"}

    out_md = OUT_DIR / f"{row['create_date']}_{aweme_id}.md"
    out_json = OUT_DIR / f"{row['create_date']}_{aweme_id}.json"
    if out_md.exists() and out_md.stat().st_size > 100:
        return {
            **row,
            "transcribe_status": "exists",
            "transcript_file": str(out_md.relative_to(ROOT)).replace("\\", "/"),
            "detected_language": "",
            "segment_count": "",
        }

    try:
        segments_iter, info = model.transcribe(
            str(video_path),
            language="zh",
            vad_filter=True,
            beam_size=5,
            word_timestamps=False,
        )
        segments = list(segments_iter)
    except Exception as exc:
        return {
            **row,
            "transcribe_status": "failed",
            "transcript_file": "",
            "detected_language": "",
            "segment_count": "0",
            "transcribe_error": f"{type(exc).__name__}: {exc}",
        }

    lines: list[str] = []
    lines.append("---")
    lines.append(f"title: Akkkk缺失视频转写-{row['create_date']}-{aweme_id}")
    lines.append("tags: [内容创作, 抖音, ASR, 视频转写]")
    lines.append("created: 2026-04-30")
    lines.append("updated: 2026-04-30")
    lines.append("sources: [Akkkk缺失视频清单.csv, Akkkk缺失视频媒体信息.csv]")
    lines.append("---")
    lines.append("")
    lines.append(f"# Akkkk缺失视频转写-{row['create_date']}-{aweme_id}")
    lines.append("")
    lines.append("## 元数据")
    lines.append("")
    lines.append(f"- aweme_id: `{aweme_id}`")
    lines.append(f"- 发布时间: {row.get('create_datetime', '')}")
    lines.append(f"- 视频链接: {row.get('aweme_url', '')}")
    lines.append(f"- 本地视频: `{video_file}`")
    lines.append(f"- 时长: {row.get('duration_seconds', '')} 秒")
    lines.append(f"- 分辨率: {row.get('width', '')}x{row.get('height', '')}")
    lines.append(f"- ASR模型: faster-whisper tiny/int8")
    lines.append(f"- 检测语言: {getattr(info, 'language', '')}")
    lines.append("")
    lines.append("## 口播原文（ASR）")
    lines.append("")
    if segments:
        for seg in segments:
            text = seg.text.strip()
            if not text:
                continue
            lines.append(f"- [{format_ts(seg.start)} - {format_ts(seg.end)}] {text}")
    else:
        lines.append("（未检测到可转写口播，可能是无声视频、音乐/画面文字为主，或音频质量不足。）")
    lines.append("")
    lines.append("## 纯文本")
    lines.append("")
    lines.append("```text")
    lines.append("".join(seg.text.strip() for seg in segments if seg.text.strip()) or "（未检测到可转写口播）")
    lines.append("```")
    lines.append("")
    lines.append("## 相关概念")
    lines.append("")
    lines.append("- [[Akkkk视频原文归档索引|Akkkk视频原文归档索引]]")
    lines.append("- [[知识库/06-内容创作与传播/Akkkk视频原文归档/Akkkk视频原文归档目录|Akkkk视频原文归档目录]]")
    out_md.write_text("\n".join(lines), encoding="utf-8")

    out_json.write_text(
        json.dumps(
            {
                "aweme_id": aweme_id,
                "language": getattr(info, "language", ""),
                "duration": getattr(info, "duration", None),
                "segments": [
                    {"start": seg.start, "end": seg.end, "text": seg.text.strip()}
                    for seg in segments
                    if seg.text.strip()
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return {
        **row,
        "transcribe_status": "ok",
        "transcript_file": str(out_md.relative_to(ROOT)).replace("\\", "/"),
        "detected_language": getattr(info, "language", ""),
        "segment_count": str(len([seg for seg in segments if seg.text.strip()])),
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    available = [row for row in rows if row.get("video_file")]
    print(f"loading model; videos={len(available)}")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")

    out_rows: list[dict[str, str]] = []
    for idx, row in enumerate(rows, 1):
        print(f"[{idx}/{len(rows)}] {row['aweme_id']}", flush=True)
        out_rows.append(transcribe_one(model, row))

    fieldnames = sorted({key for row in out_rows for key in row.keys()})
    with SUMMARY.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    ok = sum(1 for row in out_rows if row.get("transcribe_status") in {"ok", "exists"})
    print(f"transcribed={ok}/{len(out_rows)}")
    print(SUMMARY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
