import os
import shutil
import logging
import json
from datetime import datetime

# ───────────────────────────────────────────────
# ⚙️  සැකසුම් (Configuration)
# ───────────────────────────────────────────────
PATH = "/sdcard/Download/"
LOG_FILE = os.path.join(PATH, "organizer_log.txt")
HISTORY_FILE = os.path.join(PATH, ".move_history.json")

FOLDERS = {
    "Images":    [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"],
    "PDFs":      [".pdf"],
    "Videos":    [".mp4", ".mkv", ".mov", ".avi", ".wmv"],
    "Music":     [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Apps":      [".apk", ".xapk"],
    "Documents": [".docx", ".doc", ".txt", ".pptx", ".xlsx", ".csv",
                  ".md", ".toml", ".dat", ".whl"],
    "Archives":  [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Code":      [".py", ".js", ".html", ".css", ".json", ".xml",
                  ".ts", ".sh", ".zsh", ".plugin"],
    "Security":  [".keystore", ".pem", ".key", ".cert"],
}

# ───────────────────────────────────────────────
# 📋  Logging පිහිටුවීම
# ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_extension_map():
    """Extension → Folder නාමය mapping හදාගැනීම"""
    return {ext: folder for folder, exts in FOLDERS.items() for ext in exts}


def handle_duplicate(target_path):
    """
    ගොනුවක් දැනටමත් තිබේ නම්, නම වෙනස් කිරීම.
    example: file.jpg → file_1.jpg → file_2.jpg
    """
    base, ext = os.path.splitext(target_path)
    counter = 1
    while os.path.exists(target_path):
        target_path = f"{base}_{counter}{ext}"
        counter += 1
    return target_path


def load_history():
    """කලින් move කළ ෆයිල් history load කිරීම"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history):
    """History file එකට save කිරීම"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def organize(dry_run=False):
    """
    Downloads ෆෝල්ඩරය organize කිරීම.
    dry_run=True නම් ෆයිල් ගෙන නොයා preview පමණක් දක්වයි.
    """
    ext_map = get_extension_map()
    history = load_history()
    stats = {"moved": 0, "skipped": 0, "errors": 0}

    if dry_run:
        print("\n🔍 DRY RUN MODE — ෆයිල් ගෙන නොයයි, preview පමණයි:\n")

    try:
        all_files = os.listdir(PATH)
    except FileNotFoundError:
        logger.error(f"❌ ෆෝල්ඩරය හමු නොවිණ: {PATH}")
        return

    for file in all_files:
        full_path = os.path.join(PATH, file)

        # ෆෝල්ඩර් සහ hidden ෆයිල් skip කිරීම
        if not os.path.isfile(full_path) or file.startswith("."):
            continue

        _, extension = os.path.splitext(file)
        extension = extension.lower()

        folder_name = ext_map.get(extension)

        if not folder_name:
            logger.warning(f"⚠️  '{file}' — හඳුනා නොගත් ෆයිල් වර්ගය, Skip කළා.")
            stats["skipped"] += 1
            continue

        target_folder = os.path.join(PATH, folder_name)
        target_path   = os.path.join(target_folder, file)

        # Duplicate check
        if os.path.exists(target_path):
            target_path = handle_duplicate(target_path)
            logger.info(f"🔁 Duplicate — නව නම: {os.path.basename(target_path)}")

        if dry_run:
            print(f"  📄 {file}  →  {folder_name}/")
            stats["moved"] += 1
            continue

        try:
            os.makedirs(target_folder, exist_ok=True)
            shutil.move(full_path, target_path)
            logger.info(f"✅ {file} → {folder_name}/")

            # History එකට add කිරීම (undo සඳහා)
            history.append({
                "file":      os.path.basename(target_path),
                "from":      full_path,
                "to":        target_path,
                "timestamp": datetime.now().isoformat()
            })
            stats["moved"] += 1

        except Exception as e:
            logger.error(f"❌ '{file}' ගෙනයාමේ දෝෂයක්: {e}")
            stats["errors"] += 1

    if not dry_run:
        save_history(history)

    # සාරාංශය
    print("\n" + "─" * 45)
    print(f"📊 සාරාංශය")
    print(f"   ✅ Move කළා  : {stats['moved']}")
    print(f"   ⚠️  Skip කළා  : {stats['skipped']}")
    print(f"   ❌ දෝෂ       : {stats['errors']}")
    print("─" * 45)


def undo_last():
    """අවසාන organize session එක undo කිරීම"""
    history = load_history()
    if not history:
        print("⚠️  Undo කිරීමට history නැත.")
        return

    print(f"\n↩️  {len(history)} ෆයිල් ආපසු ගෙනෙමින්...\n")
    failed = 0

    for entry in reversed(history):
        try:
            if os.path.exists(entry["to"]):
                # මුල් ස්ථානයේ ෆෝල්ඩරය නැත්නම් නැවත සෑදීම
                os.makedirs(os.path.dirname(entry["from"]), exist_ok=True)
                shutil.move(entry["to"], entry["from"])
                print(f"  ↩️  {entry['file']} ආපසු ගෙනාවා.")
            else:
                print(f"  ⚠️  {entry['file']} දැනට නොමැත.")
        except Exception as e:
            print(f"  ❌ {entry['file']}: {e}")
            failed += 1

    if failed == 0:
        os.remove(HISTORY_FILE)
        print("\n✅ Undo සාර්ථකයි! History ගොනුව මකා දැමිණ.")
    else:
        print(f"\n⚠️  {failed} ෆයිල් undo කිරීමට අසාර්ථක විය.")


def show_stats():
    """ෆෝල්ඩරවල ෆයිල් ගණන සහ තරම සාරාංශ කිරීම"""
    print(f"\n📂 '{PATH}' ෆෝල්ඩරයේ වත්මන් තත්ත්වය:\n")
    for folder in FOLDERS:
        folder_path = os.path.join(PATH, folder)
        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
            size  = sum(
                os.path.getsize(os.path.join(folder_path, f))
                for f in files if os.path.isfile(os.path.join(folder_path, f))
            )
            print(f"  📁 {folder:<12} — {len(files):>4} ෆයිල්  ({size/1024:.1f} KB)")
    print()


# ───────────────────────────────────────────────
# 🚀  ප්‍රධාන menu
# ───────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 45)
    print("   📁 File Organizer — Downloads Cleaner")
    print("=" * 45)
    print("  1. Organize කිරීම (ෆයිල් move කරයි)")
    print("  2. Preview කිරීම (Dry Run)")
    print("  3. Undo — ආපසු ගෙනෙමු")
    print("  4. Stats — ෆෝල්ඩර තත්ත්වය")
    print("  5. වැසීම")
    print("─" * 45)

    choice = input("ඔබගේ තේරීම (1-5): ").strip()

    if choice == "1":
        organize()
    elif choice == "2":
        organize(dry_run=True)
    elif choice == "3":
        undo_last()
    elif choice == "4":
        show_stats()
    elif choice == "5":
        print("👋 වැසිණ.")
    else:
        print("⚠️  වලංගු නොවන තේරීමකි.")
