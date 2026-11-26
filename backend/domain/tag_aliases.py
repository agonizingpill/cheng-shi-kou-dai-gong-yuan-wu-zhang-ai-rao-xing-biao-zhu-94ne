"""同义标记合并的纯逻辑：归一化、权重取舍与旧分作废判定。

规则保证扁平：旧称不会同时是别条规则的新叫法，新叫法也不会再被合并，
因此一层映射即可解析，无需链式展开。
"""


def alias_map(rules):
    """规则行列表 → {旧称: 新叫法}。"""
    return {row['alias']: row['canonical'] for row in rules}


def normalize_tags(tags, mapping):
    """入口障碍标记归一化并保序去重：同一障碍两种叫法都报也只算一次。"""
    merged = []
    for tag in tags:
        name = mapping.get(tag, tag)
        if name not in merged:
            merged.append(name)
    return merged


def normalize_profile(avoid, weights, mapping):
    """偏好卡归一化：同一新叫法的重复项只保留较重的那项权重。"""
    merged = {}
    avoid = normalize_tags(avoid, mapping)
    for name in avoid:
        merged[name] = 0
    for name, weight in weights.items():
        canonical = mapping.get(name, name)
        if canonical in merged:
            merged[canonical] = max(merged[canonical], weight)
    return avoid, merged


def affected(rules, since_serial, tags):
    """序号大于 since_serial 的规则中，是否有波及这些标记的（用于作废旧分）。"""
    names = set(tags)
    return any(rule['serial'] > since_serial and {rule['alias'], rule['canonical']} & names
               for rule in rules)
