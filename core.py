import sys
from constants import validate_style, validate_event, validate_level, LEVEL_ORDER
from storage import load_data, save_data


def add_member(member_id, name, phone, style, level):
    validate_style(style)
    validate_level(level)

    data = load_data()
    if member_id in data["members"]:
        print(f"错误: 队员 {member_id} 已存在", file=sys.stderr)
        sys.exit(1)

    data["members"][member_id] = {
        "id": member_id,
        "name": name,
        "phone": phone,
        "style": style,
        "level": level,
        "promotions": [],
    }
    save_data(data)
    print(f"已添加队员: {member_id} {name} ({style}, {level})")


def record_score(member_id, event, score, date, competition):
    validate_event(event)

    data = load_data()
    if member_id not in data["members"]:
        print(f"错误: 队员 {member_id} 不存在", file=sys.stderr)
        sys.exit(1)

    data["scores"].append({
        "member_id": member_id,
        "event": event,
        "score": float(score),
        "date": date,
        "competition": competition,
    })
    save_data(data)
    print(f"已记录成绩: {member_id} {event} {score}分 ({date} {competition})")


def promote(member_id, to_level, date):
    validate_level(to_level)

    data = load_data()
    if member_id not in data["members"]:
        print(f"错误: 队员 {member_id} 不存在", file=sys.stderr)
        sys.exit(1)

    member = data["members"][member_id]
    current_level = member["level"]

    if LEVEL_ORDER[to_level] <= LEVEL_ORDER[current_level]:
        print(f"错误: 只能向更高级别晋升 (当前: {current_level}, 目标: {to_level})", file=sys.stderr)
        sys.exit(1)

    member["level"] = to_level
    member["promotions"].append({
        "from": current_level,
        "to": to_level,
        "date": date,
    })
    save_data(data)
    print(f"段位晋升: {member_id} {current_level} -> {to_level} ({date})")


def member_stats(member_id):
    data = load_data()
    if member_id not in data["members"]:
        print(f"错误: 队员 {member_id} 不存在", file=sys.stderr)
        sys.exit(1)

    member = data["members"][member_id]
    scores = [s for s in data["scores"] if s["member_id"] == member_id]

    print(f"队员: {member['name']} ({member_id})")
    print(f"武术风格: {member['style']}")
    print(f"当前段位: {member['level']}")

    if not scores:
        print("暂无比赛成绩")
        return

    all_scores = [s["score"] for s in scores]
    print(f"历史最高分: {max(all_scores)}")

    event_scores = {}
    for s in scores:
        event_scores.setdefault(s["event"], []).append(s["score"])

    print("各项目平均分:")
    for event, vals in event_scores.items():
        avg = sum(vals) / len(vals)
        print(f"  {event}: {avg:.1f} (参赛 {len(vals)} 次)")


def monthly_scores(month):
    data = load_data()
    prefix = month
    scores = [s for s in data["scores"] if s["date"].startswith(prefix)]

    if not scores:
        print(f"{month} 无比赛成绩记录")
        return

    event_scores = {}
    for s in scores:
        event_scores.setdefault(s["event"], []).append(s["score"])

    print(f"{month} 月度成绩统计:")
    for event, vals in event_scores.items():
        avg = sum(vals) / len(vals)
        print(f"  {event}: 参赛人次 {len(vals)}, 平均分 {avg:.1f}")
