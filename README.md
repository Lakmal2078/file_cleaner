# 📁 File Organizer — Downloads Cleaner

ඔබගේ Android Downloads ෆෝල්ඩරය ස්වයංක්‍රීයව **ෆයිල් වර්ගය අනුව** ඉබේම sort කරන Python script එකක්.  
[Termux](https://termux.dev) හරහා Android දුරකථනයේ සෘජුවම ධාවනය කළ හැකිය.

---

## ✨ Features

| Feature | විස්තරය |
|---|---|
| 🗂️ Auto Organize | ෆයිල් extension අනුව ෆෝල්ඩරවලට move කරයි |
| 🔍 Dry Run | ෆයිල් ගෙන නොයා preview පෙන්වයි |
| ↩️ Undo | ෆයිල් මුල් ස්ථානවලට ආපසු ගෙනෙයි |
| 📊 Stats | ෆෝල්ඩර ගණන සහ KB දක්වයි |
| 🔁 Duplicate Handling | `file.jpg` → `file_1.jpg` ලෙස rename කරයි |
| 📋 Logging | `organizer_log.txt` ගොනුවට සියල්ල සටහන් කරයි |

---

## 📂 ෆෝල්ඩර ව්‍යුහය

```
Downloads/
├── Images/       → .jpg .jpeg .png .gif .webp .bmp .svg
├── PDFs/         → .pdf
├── Videos/       → .mp4 .mkv .mov .avi .wmv
├── Music/        → .mp3 .wav .aac .flac .ogg
├── Apps/         → .apk .xapk
├── Documents/    → .docx .txt .csv .md .toml .dat .whl
├── Archives/     → .zip .rar .tar .gz .7z
├── Code/         → .py .js .html .ts .sh .zsh .json .xml
└── Security/     → .keystore .pem .key .cert
```

---

## 🚀 ස්ථාපනය (Installation)

### අවශ්‍යතා
- [Termux](https://f-droid.org/packages/com.termux/) (Android)
- Python 3.x

### පියවර

```bash
# 1. Termux හි Python install කිරීම
pkg install python

# 2. Storage permission ලබාගැනීම
termux-setup-storage

# 3. Script ෆෝල්ඩරයක් සෑදීම
mkdir ~/my_script
cd ~/my_script

# 4. file_cleaner.py ගොනුව මෙම ෆෝල්ඩරයට copy කිරීම
```

---

## ▶️ භාවිතය (Usage)

```bash
cd ~/my_script
python file_cleaner.py
```

Menu එකෙන් option එකක් තෝරන්න:

```
=============================================
   📁 File Organizer — Downloads Cleaner
=============================================
  1. Organize කිරීම (ෆයිල් move කරයි)
  2. Preview කිරීම (Dry Run)
  3. Undo — ආපසු ගෙනෙමු
  4. Stats — ෆෝල්ඩර තත්ත්වය
  5. වැසීම
```

### 💡 Tips

- **පළමු වතාවේ** `2. Preview` option එකෙන් test කරන්න.
- **Undo** option එක ක්‍රියා කරන්නේ **වරක් පමණි** — organize කළ වහාම undo කරන්නේ නම් පමණයි.
- `organizer_log.txt` ගොනුව Documents/ ෆෝල්ඩරයට move වේ — ඒ ගැන බිය නොවන්න.

---

## ⚙️ Path වෙනස් කිරීම

`file_cleaner.py` ගොනුවේ මෙම line එක සොයාගෙන වෙනස් කරන්න:

```python
# Default (Termux)
PATH = "/sdcard/Download/"

# විකල්ප
PATH = "/storage/emulated/0/Download/"   # සමහර Android versions
PATH = "/storage/emulated/0/Documents/"  # Documents ෆෝල්ඩරය
```

---

## 📝 නව Extensions එකතු කිරීම

`FOLDERS` dict එකට අලුත් extension එකක් එකතු කිරීම ඉතා පහසුයි:

```python
FOLDERS = {
    "Images": [".jpg", ".png", ".heic"],  # ← .heic එකතු කළා
    # ...
    "eBooks": [".epub", ".mobi"],         # ← නව category
}
```

---

## 🗃️ ගොනු විස්තරය

| ගොනුව | විස්තරය |
|---|---|
| `file_cleaner.py` | ප්‍රධාන script ගොනුව |
| `organizer_log.txt` | සියලු move actions log (Documents/ වෙත යවයි) |
| `.move_history.json` | Undo සඳහා hidden history ගොනුව |

---

## ⚠️ වැදගත් සටහන්

- `.keystore` ගොනු **Security/** ෆෝල්ඩරයට move වේ — APK signing keys ආරක්ෂිතව තබාගන්න.
- Script එක **Downloads ෆෝල්ඩරයේ ෆෝල්ඩර** (subdirectories) ස්පර්ශ නොකරයි — ෆයිල් පමණි.
- Hidden ගොනු (`.` දිය) automatically skip වේ.

---

## 🛠️ නිර්මාතෘ

Termux + Python project — Android Downloads folder management සඳහා.
