#!/usr/bin/env python3
import os, json, argparse, urllib.request

GATE_BUTTONS = {
    "gate_1_plan": [
        [{"text": "✅ Chọn Angle 1", "callback_data": "G1_A1"},
         {"text": "✅ Chọn Angle 2", "callback_data": "G1_A2"}],
        [{"text": "✅ Chọn Angle 3", "callback_data": "G1_A3"},
         {"text": "❌ Bỏ qua / Làm lại", "callback_data": "G1_REJECT"}]
    ],
    "gate_2_shoot": [
        [{"text": "📹 Đã thả Clip thô lên Drive", "callback_data": "G2_UPLOADED"}]
    ],
    "gate_3_publish": [
        [{"text": "🚀 Duyệt & Đăng Ngay", "callback_data": "G3_PUBLISH_NOW"}],
        [{"text": "⏰ Hẹn giờ 19h30", "callback_data": "G3_SCHEDULE"},
         {"text": "✏️ Yêu cầu sửa", "callback_data": "G3_EDIT"}]
    ]
}

def send_telegram_gate(gate, content_id, text):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print(f"[TELEGRAM GATE SIMULATION: {gate} | {content_id}]\n{text}")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "reply_markup": {"inline_keyboard": GATE_BUTTONS[gate]}}
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode("utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", required=True, choices=["gate_1_plan", "gate_2_shoot", "gate_3_publish"])
    parser.add_argument("--content-id", required=True)
    parser.add_argument("--message-file", required=True)
    args = parser.parse_args()
    with open(args.message_file, "r", encoding="utf-8") as f:
        send_telegram_gate(args.gate, args.content_id, f.read())
