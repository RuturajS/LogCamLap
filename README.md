Here’s a clean, no-BS **README.md** you can use for your project:

---

```markdown
# 📸 Laptop Access Monitoring System

A simple Python-based security tool that captures an image using your webcam whenever your laptop is accessed (login/unlock), saves it locally, and sends it to a Discord channel via webhook.

It also works offline — images are queued and sent later when internet is available.

---

## 🚀 Features

- 📸 Automatic webcam capture
- 💾 Local image storage
- 🌐 Discord webhook integration
- 🔁 Offline queue + retry system
- 📝 Logging for debugging (`app.log`)
- ⚙️ Works with Windows Task Scheduler

---

## 📂 Project Structure

```

LogDetail/
├── captures/        # Saved images
├── pending.json     # Queue of unsent images
├── app.log          # Logs
└── script.py        # Main script

```

---

## 🧰 Requirements

Create a `requirements.txt`:

```

opencv-python
requests

````

Install dependencies:

```bash
pip install -r requirements.txt
````

---

## ⚙️ Configuration

Edit the script and set:

```python
BASE_DIR = r"C:\Users\YourUser\Pictures\LogDetail"
WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK"
```

---

## ▶️ Run Manually (Test First)

```bash
python script.py
```

Check:

* Image saved in `captures/`
* Logs written in `app.log`

---

## 🕒 Automate with Task Scheduler

### 1. Open Task Scheduler

```
Win + R → taskschd.msc
```

### 2. Create Task

#### General:

* Run only when user is logged on ✅
* Run with highest privileges ✅

#### Triggers:

* At log on
* On workstation unlock

#### Actions:

* Program:

```
pythonw.exe
```

* Arguments:

```
"path\to\script.py"
```

* Start in:

```
script folder path
```

---

## 🔇 Run Silently (No CMD Window)

Use `pythonw.exe` instead of `python.exe`.

If using `.bat`:

```bat
@echo off
start "" "path\to\pythonw.exe" "path\to\script.py"
exit
```

---

## 🔁 How Offline Mode Works

* If no internet:

  * Image saved locally
  * Added to `pending.json`
* When internet returns:

  * Old images are automatically sent

---

## 🐛 Troubleshooting

### No image captured

* Camera in use by another app
* Try changing:

```python
cv2.VideoCapture(1)
```

---

### Script not running from scheduler

* Check Task History
* Verify Python path
* Ensure "Start in" path is set

---

### No Discord messages

* Check webhook URL
* Check `app.log` for status codes

---

### No logs generated

* Script not running OR wrong directory

---

## ⚠️ Limitations

* Can be bypassed if:

  * Camera is covered
  * System is booted externally
  * Task Scheduler is disabled

👉 This is **monitoring**, not full security.

---

---

## 📌 Final Note

Test everything manually before relying on automation.
If logs don’t update → your setup is broken, not the script.

