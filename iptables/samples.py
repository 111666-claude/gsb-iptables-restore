"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "table":
        text = "*filter\n-A INPUT -j ACCEPT\nCOMMIT\n*nat\n-A PREROUTING -j DROP\nCOMMIT\n"
        ruleset = core.parse(text, core.Counter())
        _line({"tables": len(ruleset.tables)})
        return 0
    if name == "policy":
        text = "*filter\n:INPUT DROP [0:0]\nCOMMIT\n"
        ruleset = core.parse(text, core.Counter())
        policy = ruleset.chains[0]["policy"] if ruleset.chains else ""
        _line({"policy": policy})
        return 0
    if name == "dup":
        text = "*filter\n-A INPUT -j ACCEPT\n-A INPUT -j ACCEPT\nCOMMIT\n"
        ruleset = core.parse(text, core.Counter())
        _line({"rules": len(ruleset.rules)})
        return 0
    if name == "counter":
        text = "*filter\n:INPUT DROP [10:200]\nCOMMIT\n"
        ruleset = core.parse(text, core.Counter())
        policy = ruleset.chains[0]["policy"] if ruleset.chains else ""
        _line({"has_digits": any(ch.isdigit() for ch in policy)})
        return 0
    if name == "work":
        lines = ["*filter"]
        for i in range(800):
            lines.append("-A c%04d -j ACCEPT" % i)
        lines.append("COMMIT")
        ruleset = core.parse("\n".join(lines) + "\n", core.Counter())
        counter = core.Counter()
        for i in range(800):
            core.rules_in(ruleset, "c%04d" % i, counter)
        _line({"rules": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
