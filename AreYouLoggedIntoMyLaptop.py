import cv2
import requests
import os
import json
import logging
from datetime import datetime

# ================= CONFIG =================
BASE_DIR = r"C:\Users\path\path\Pictures\LogDetail"
CAPTURE_DIR = os.path.join(BASE_DIR, "captures")
QUEUE_FILE = os.path.join(BASE_DIR, "pending.json")
LOG_FILE = os.path.join(BASE_DIR, "app.log")
WEBHOOK_URL = "https://discord.com/api/webhooks/Your Webhook  Add here"

os.makedirs(CAPTURE_DIR, exist_ok=True)

# ================= LOGGING =================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log(msg):
    print(msg)
    logging.info(msg)

# ================= HELPERS =================

def is_internet_available():
    try:
        requests.get("https://1.1.1.1", timeout=3)
        return True
    except Exception as e:
        log(f"Internet check failed: {e}")
        return False

def load_queue():
    try:
        if os.path.exists(QUEUE_FILE):
            with open(QUEUE_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        log(f"Queue load error: {e}")
    return []

def save_queue(queue):
    try:
        with open(QUEUE_FILE, "w") as f:
            json.dump(queue, f, indent=2)
    except Exception as e:
        log(f"Queue save error: {e}")

def capture_image():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            log("❌ Camera capture failed")
            return None

        filename = datetime.now().strftime("intruder_%Y%m%d_%H%M%S.jpg")
        path = os.path.join(CAPTURE_DIR, filename)
        cv2.imwrite(path, frame)

        log(f"📸 Captured: {path}")
        return path

    except Exception as e:
        log(f"Capture error: {e}")
        return None

def send_to_discord(filepath):
    try:
        with open(filepath, "rb") as f:
            response = requests.post(WEBHOOK_URL, files={"file": f}, timeout=10)

        log(f"Discord response: {response.status_code}")
        return response.status_code in [200, 204]

    except Exception as e:
        log(f"Send error: {e}")
        return False

# ================= CORE =================

def process_queue():
    queue = load_queue()
    if not queue:
        log("Queue empty")
        return

    log(f"🔄 Retrying {len(queue)} pending files")

    new_queue = []
    for filepath in queue:
        if os.path.exists(filepath):
            if send_to_discord(filepath):
                log(f"✅ Sent from queue: {filepath}")
            else:
                new_queue.append(filepath)
        else:
            log(f"⚠️ Missing file: {filepath}")

    save_queue(new_queue)

def main():
    log("==== Script started ====")

    # Step 1: ALWAYS capture
    filepath = capture_image()
    if not filepath:
        log("Capture failed — exiting")
        return

    queue = load_queue()

    # Step 2: Try sending (never block flow)
    if is_internet_available():
        log("🌐 Internet available")

        if send_to_discord(filepath):
            log("✅ Sent successfully")
        else:
            log("⚠️ Send failed — queued")
            queue.append(filepath)
    else:
        log("❌ No internet — queued")
        queue.append(filepath)

    save_queue(queue)

    # Step 3: Retry old queue
    if is_internet_available():
        process_queue()

    log("==== Script finished ====")

# ================= RUN =================

if __name__ == "__main__":
    main()
