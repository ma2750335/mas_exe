# -*- coding: utf-8 -*-
"""
sync_from_lib.py
從 mas_lib/mas 同步到 mas_exe/mas，並套用 exe-specific 的設定。

使用方式：
    python sync_from_lib.py           # 預覽模式（dry-run，只顯示變更）
    python sync_from_lib.py --apply   # 實際執行同步
"""

import sys
import shutil
import filecmp
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── 路徑設定 ────────────────────────────────────────────────────────────────
SRC = Path("C:/workplace/mas_lib/mas")
DST = Path("C:/workplace/mas_exe/mas")

# 不同步的資料夾（相對於 mas/）
SKIP_DIRS = {"backtest", "docs", "reporting", "__pycache__"}

# 不同步的副檔名
SKIP_EXTS = {".pyc"}

# 不同步的特定檔案（相對於 mas/，使用 posix 路徑格式）
SKIP_FILES = {
    "history/history_data_to_db.py",
    "history/history_data_db.py",
    "clinet/client_post_real.py",
    "clinet/client_post_real_bk.py"
}

# ── exe-specific patch ───────────────────────────────────────────────────────
# 格式：(相對路徑, 要搜尋的字串, 要替換的字串)
PATCHES = [
    (
        "enum/env_setting.py",
        "exe = False",
        "exe = True",
    ),
    (
        "clinet/client_post.py",
        "from mas.clinet.client_post_real import ClientPostReal",
        "from mas.clinet.client_post_real_exe import ClientPostReal",
    ),
]


# ── 工具函式 ─────────────────────────────────────────────────────────────────
def should_skip(rel: Path) -> bool:
    """判斷是否要跳過這個路徑。"""
    parts = rel.parts
    # 跳過指定資料夾（含子目錄）
    if parts[0] in SKIP_DIRS:
        return True
    # 跳過指定副檔名
    if rel.suffix in SKIP_EXTS:
        return True
    # 跳過特定檔案
    if rel.as_posix() in SKIP_FILES:
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


def apply_patches(dst: Path, dry_run: bool):
    """套用 exe-specific 的字串替換。"""
    for rel_str, old, new in PATCHES:
        target = dst / rel_str
        if not target.exists():
            print(f"  [PATCH] 檔案不存在，跳過：{rel_str}")
            continue

        content = target.read_text(encoding="utf-8")
        if old not in content:
            if new in content:
                print(f"  [PATCH] 已是正確狀態：{rel_str}")
            else:
                print(f"  [PATCH] 找不到替換目標，請手動確認：{rel_str}")
            continue

        new_content = content.replace(old, new)
        if dry_run:
            print(f"  [PATCH] {rel_str}")
            print(f"          - {old}")
            print(f"          + {new}")
        else:
            target.write_text(new_content, encoding="utf-8")
            print(f"  [PATCH] 已套用：{rel_str}  ({old!r} → {new!r})")


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

    print()
    print("套用 exe-specific patch：")
    apply_patches(DST, dry_run)

    if dry_run:
        print()
        print("※ 預覽模式，未實際修改任何檔案。加上 --apply 執行同步。")


# ── 主程式 ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="從 mas_lib 同步 mas 到 mas_exe")
    parser.add_argument(
        "--apply", action="store_true", help="實際執行同步（預設為 dry-run 預覽）"
    )
    args = parser.parse_args()

    sync(dry_run=not args.apply)
