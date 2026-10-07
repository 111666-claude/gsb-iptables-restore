"""解析 iptables-restore 规则集。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


class Ruleset:
    def __init__(self):
        self.rules = []
        self.chains = []
        self.tables = []


def parse(text, counter):
    ruleset = Ruleset()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        counter.scanned += 1
        if line.startswith("*") or line == "COMMIT":
            continue
        if line.startswith(":"):
            parts = line[1:].split()
            ruleset.chains.append({"name": parts[0], "policy": " ".join(parts[1:])})
            continue
        if line.startswith("-A"):
            ruleset.rules.append(line)
    return ruleset


def rules_in(ruleset, chain, counter):
    out = []
    for rule in ruleset.rules:
        counter.scanned += 1
        if rule.split()[1] == chain:
            out.append(rule)
    return out
