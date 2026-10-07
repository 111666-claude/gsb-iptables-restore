# iptables-restore

解析 iptables-restore 规则集：表段、链声明与策略、计数器、规则去重，以及按表与链汇总。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m iptables --sample=table
python3 -m iptables --sample=policy
python3 -m iptables --sample=dup
python3 -m iptables --sample=counter
python3 -m iptables --sample=work
```

## 口径

- **表**：`*名字` 开一段，`COMMIT` 结束；规则归入当前表。
- **链**：`:` 开头声明链，格式 `:名字 策略 [包数:字节数]`；内置链有策略，自定义链策略是 `-`。
- **规则**：`-A 链 参数...`；同一条规则在同一表同一链里重复出现只算一条。
- **计数器**：方括号里是包数与字节数，两个整数。
- **查找**：按表与链汇总走索引。

## 不变量

- 每条规则都属于声明过的表；同表同链的规则无重复。
- 链声明的计数器是整数对。
- `scanned` 不随规则数乘查询次数放大：八百条规则的 `scanned` 不超过 6000。

## 输出契约

`Ruleset` 含表到链声明与规则的映射。场景打印一行 JSON。
`--sample=work` 打印 `{"rules": N, "scanned": N}`。
