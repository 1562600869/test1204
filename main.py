import argparse
import sys
import core
from constants import VALID_STYLES, VALID_EVENTS, VALID_LEVELS, validate_month


def main():
    parser = argparse.ArgumentParser(description="业余武术队队员训练成绩和段位管理工具")
    subparsers = parser.add_subparsers(dest="command")

    p_add = subparsers.add_parser("add-member", help="添加队员")
    p_add.add_argument("member_id", help="队员编号")
    p_add.add_argument("name", help="姓名")
    p_add.add_argument("--phone", required=True, help="联系电话")
    p_add.add_argument("--style", required=True, choices=VALID_STYLES, help="武术风格: 长拳/太极/南拳/器械")
    p_add.add_argument("--level", required=True, choices=VALID_LEVELS, help="段位: 初学/一级/二级/三级/四级/五级")

    p_score = subparsers.add_parser("record-score", help="记录比赛成绩")
    p_score.add_argument("member_id", help="队员编号")
    p_score.add_argument("--event", required=True, choices=VALID_EVENTS, help="比赛项目: 套路/散打/器械")
    p_score.add_argument("--score", required=True, type=float, help="成绩(浮点数)")
    p_score.add_argument("--date", required=True, help="比赛日期")
    p_score.add_argument("--competition", required=True, help="比赛名称")

    p_promote = subparsers.add_parser("promote", help="段位晋升")
    p_promote.add_argument("member_id", help="队员编号")
    p_promote.add_argument("--to-level", required=True, choices=VALID_LEVELS, help="目标段位")
    p_promote.add_argument("--date", required=True, help="晋升日期")

    p_stats = subparsers.add_parser("member-stats", help="队员统计")
    p_stats.add_argument("member_id", help="队员编号")

    p_monthly = subparsers.add_parser("monthly-scores", help="月度成绩统计")
    p_monthly.add_argument("--month", required=True, help="月份(如 2024-03)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "add-member":
        core.add_member(args.member_id, args.name, args.phone, args.style, args.level)
    elif args.command == "record-score":
        core.record_score(args.member_id, args.event, args.score, args.date, args.competition)
    elif args.command == "promote":
        core.promote(args.member_id, args.to_level, args.date)
    elif args.command == "member-stats":
        core.member_stats(args.member_id)
    elif args.command == "monthly-scores":
        validate_month(args.month)
        core.monthly_scores(args.month)


if __name__ == "__main__":
    main()
