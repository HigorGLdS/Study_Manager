from datetime import datetime, timedelta


def weekly_stats(materials):
    today = datetime.now()
    week = today - timedelta(days=7)

    valid = []
    for m in materials:
        date = m.get("updated_at")
        if not date:
            continue
        if datetime.fromisoformat(date) >= week:
            valid.append(m)

    if not valid:
        return 0, 0

    avg = sum(m["progress"] for m in valid) // len(valid)
    done = sum(1 for m in valid if m["progress"] == 100)

    return avg, int(done / len(valid) * 100)