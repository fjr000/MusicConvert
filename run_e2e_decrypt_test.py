# -*- coding: utf-8 -*-
"""端到端解密测试：调用 app.decryptor 解密真实/合成加密样本，并用 ffprobe 验证输出。"""
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

from app.decryptor import decrypt_audio_to_temp, cleanup_decrypted_path, DecryptError
from app.ffmpeg_tools import get_ffprobe_path

SAMPLES_DIR = Path(".trellis/tasks/archive/2026-06/06-11-format-evaluation/scratch/encrypted-samples")

TARGETS = [
    # 真实 KGM 文件
    Path("Lost Frequencies、Janieck - Reality.kgm"),
    Path("徐梦圆 - China-X.kgm"),
    Path("越人歌 (钢琴伴奏).kgm"),
    # 合成 KGM 样本 (v2/v3/v4)
    SAMPLES_DIR / "test_kgm_v2.kgm",
    SAMPLES_DIR / "test_kgm_v3.kgm",
    SAMPLES_DIR / "test_kgm_v4.kgm",
    # QQ音乐 QMC 系列
    SAMPLES_DIR / "test_qmc1.qmcogg",
    SAMPLES_DIR / "test_qmc2_map.mgg",
    SAMPLES_DIR / "test_qmc2_rc4.mgg",
    SAMPLES_DIR / "test_qmc2_rc4_EncV2.mgg",
    # 喜马拉雅（顺带）
    SAMPLES_DIR / "test_xmly.x2m",
    SAMPLES_DIR / "test_xmly.x3m",
]


def probe(path: Path) -> str:
    cmd = [
        str(get_ffprobe_path()),
        "-v", "error",
        "-show_entries", "format=format_name,duration",
        "-of", "csv=p=0",
        str(path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return f"PROBE-FAIL: {result.stderr.strip()[:120]}"
    return result.stdout.strip()


def main():
    results = []
    for target in TARGETS:
        name = target.name
        if not target.exists():
            results.append((name, "MISSING", ""))
            continue
        try:
            out = decrypt_audio_to_temp(target)
            info = probe(out)
            size = out.stat().st_size
            status = "OK" if not info.startswith("PROBE-FAIL") else "DECRYPTED-BUT-INVALID"
            results.append((name, status, f"{out.suffix} {size}B {info}"))
            cleanup_decrypted_path(out)
        except DecryptError as exc:
            results.append((name, "DECRYPT-FAIL", str(exc)))
        except Exception as exc:
            results.append((name, "ERROR", f"{type(exc).__name__}: {exc}"))

    print()
    width = max(len(r[0]) for r in results) + 2
    for name, status, detail in results:
        print(f"{name:<{width}} {status:<22} {detail}")

    failed = [r for r in results if r[1] not in ("OK",)]
    print(f"\n总计: {len(results)}, 通过: {len(results) - len(failed)}, 未通过: {len(failed)}")


if __name__ == "__main__":
    main()
