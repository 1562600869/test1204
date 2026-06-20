import sys

VALID_STYLES = ("长拳", "太极", "南拳", "器械")
VALID_EVENTS = ("套路", "散打", "器械")
VALID_LEVELS = ("初学", "一级", "二级", "三级", "四级", "五级")
LEVEL_ORDER = {level: idx for idx, level in enumerate(VALID_LEVELS)}


def validate_style(style):
    if style not in VALID_STYLES:
        print(f"错误: 武术风格只能是 {('/').join(VALID_STYLES)}", file=sys.stderr)
        sys.exit(1)


def validate_event(event):
    if event not in VALID_EVENTS:
        print(f"错误: 比赛项目只能是 {('/').join(VALID_EVENTS)}", file=sys.stderr)
        sys.exit(1)


def validate_level(level):
    if level not in VALID_LEVELS:
        print(f"错误: 段位只能是 {('/').join(VALID_LEVELS)}", file=sys.stderr)
        sys.exit(1)
