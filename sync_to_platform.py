# -*- coding: utf-8 -*-
"""
sync_to_platform.py
將 mas_exe/ 同步到 mas_platform_dev/server/mas_lib/exe/。

使用方式：
    python sync_to_platform.py           # 預覽模式（dry-run，只顯示變更）
    python sync_to_platform.py --apply   # 實際執行同步
"""

import sys
import shutil
import filecmp
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── 路徑設定 ────────────────────────────────────────────────────────────────
SRC = Path("C:/workplace/mas_exe")
DST = Path("C:/workplace/mas_platform_dev/server/mas_lib/exe")

# 不同步的資料夾（相對於 mas_exe/）
SKIP_DIRS = {".git", "__pycache__", "build", "dist"}

# 不同步的副檔名
SKIP_EXTS = {".pyc", ".spec"}

# 不同步的特定檔案
SKIP_FILES = {".gitignore"}


# ── 工具函式 ─────────────────────────────────────────────────────────────────
def should_skip(rel: Path) -> bool:
    """判斷是否要跳過這個路徑。"""
    parts = rel.parts
    # 跳過指定資料夾（含子目錄）
    if parts[0] in SKIP_DIRS:
        return True
    # 跳過副檔名
    if rel.suffix in SKIP_EXTS:
        return True
    # 跳過特定檔案
    if rel.name in SKIP_FILES:
        return True
    return False


def collect_src_files(src: Path) -> list[Path]:
    """收集 src 下所有要同步的檔案（相對路徑）。"""
    result = []
    for path in src.rglob("*"):
        if path.is_file():
            rel = path.relative_to(src)
            if not should_skip(rel):
                result.append(rel)
    return sorted(result)


def sync(dry_run: bool):
    print(f"來源：{SRC}")
    print(f"目標：{DST}")
    print(f"模式：{'預覽 (dry-run)' if dry_run else '實際執行'}")
    print("=" * 60)

    files = collect_src_files(SRC)

    copied = []
    skipped_same = []

    for rel in files:
        src_file = SRC / rel
        dst_file = DST / rel

        # 目標資料夾不存在時建立
        if not dry_run:
            dst_file.parent.mkdir(parents=True, exist_ok=True)

        if dst_file.exists() and filecmp.cmp(src_file, dst_file, shallow=False):
            skipped_same.append(rel)
            continue

        action = "新增" if not dst_file.exists() else "更新"
        copied.append((rel, action))
        if dry_run:
            print(f"  [{action}] {rel}")
        else:
            shutil.copy2(src_file, dst_file)
            print(f"  [{action}] {rel}")

    print()
    print(f"同步完成：{len(copied)} 個檔案變更，{len(skipped_same)} 個相同跳過")

    if dry_run:
        print()
        print("※ 預覽模式，未實際修改任何檔案。加上 --apply 執行同步。")


# ── 主程式 ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="將 mas_exe 同步到 mas_platform_dev")
    parser.add_argument(
        "--apply", action="store_true", help="實際執行同步（預設為 dry-run 預覽）"
    )
    args = parser.parse_args()

    sync(dry_run=not args.apply)
