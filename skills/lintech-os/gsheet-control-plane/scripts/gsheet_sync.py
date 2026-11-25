#!/usr/bin/env python3
import os, json, argparse, datetime

def main():
    parser = argparse.ArgumentParser(description="LinTech GSheet Control Plane CLI")
    parser.add_argument("--action", required=True, choices=["read_memory", "update_status", "upsert_memory"])
    parser.add_argument("--content-id", default="")
    parser.add_argument("--status", default="")
    parser.add_argument("--angle", default="")
    parser.add_argument("--key", default="")
    parser.add_argument("--value", default="")
    parser.add_argument("--agent", default="orchestrator")
    args = parser.parse_args()

    now = datetime.datetime.now().isoformat()
    local_db = os.path.expanduser("~/.hermes/lintech_control_plane_db.json")
    if not os.path.exists(local_db):
        default_data = {
            "Brand_Memory": {
                "BRAND_PERSONA": {"Value": "Chuyên gia AI thực chiến, điềm đạm, sắc bén, không lý thuyết suông", "Updated_At": now, "Source_Agent": "init"},
                "PRONOUNS": {"Value": "Mình - Bạn", "Updated_At": now, "Source_Agent": "init"},
                "FORBIDDEN_WORDS": {"Value": "Trong kỷ nguyên số, hãy cùng khám phá, đừng lo lắng, chìa khóa vàng, không chỉ... mà còn", "Updated_At": now, "Source_Agent": "init"},
                "WINNING_HOOKS": {"Value": "[Phản bác niềm tin phổ biến] + [Ẩn dụ tuyển thực tập sinh]", "Updated_At": now, "Source_Agent": "init"}
            },
            "Content_Pipeline": {},
            "Performance_KPI": {}
        }
        with open(local_db, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)

    with open(local_db, "r", encoding="utf-8") as f:
        db = json.load(f)

    if args.action == "read_memory":
        print(json.dumps(db.get("Brand_Memory", {}), ensure_ascii=False, indent=2))
    elif args.action == "update_status":
        db.setdefault("Content_Pipeline", {})[args.content_id] = {
            "Status": args.status,
            "Angle_Selected": args.angle,
            "Updated_At": now
        }
        with open(local_db, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        print(f"[OK] {args.content_id} -> {args.status}")
    elif args.action == "upsert_memory":
        db.setdefault("Brand_Memory", {})[args.key] = {
            "Value": args.value,
            "Updated_At": now,
            "Source_Agent": args.agent
        }
        with open(local_db, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        print(f"[OK] Brand_Memory[{args.key}] updated by {args.agent}")

if __name__ == "__main__":
    main()
