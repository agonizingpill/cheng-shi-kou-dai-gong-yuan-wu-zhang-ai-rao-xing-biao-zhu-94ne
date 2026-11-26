from sqlalchemy import func, select

from core.records import insert, need, scan, update
from domain import tag_aliases as aliases
from domain.entrances_model import entrances
from domain.tag_aliases_model import tag_aliases
from domain.walk_profiles_model import walk_profiles

STALE_DETAIL = '匹配分受标记合并规则更新影响已作废，请重新计算后再交线路单'


def current_serial(conn):
    return conn.scalar(select(func.max(tag_aliases.c.serial))) or 0


def stale_message(conn, payload):
    """计算任务提交后又有波及这些标记的合并规则，则旧分作废。"""
    profile = payload.get('profile') or {}
    involved = set(profile.get('avoid') or [])
    for row in payload.get('entrances') or []:
        involved.update(row.get('tags') or [])
    if aliases.affected(scan(conn, tag_aliases), payload.get('rule_serial') or 0, involved):
        return STALE_DETAIL
    return None


def merge_tags(conn, user, data):
    need(data.alias != data.canonical, '旧称与新叫法相同，无需合并')
    rules = scan(conn, tag_aliases)
    mapping = aliases.alias_map(rules)
    need(data.alias not in mapping, '该旧称已有合并规则')
    need(data.canonical not in mapping, '新叫法本身已被合并，请直接使用最终叫法')
    need(data.alias not in set(mapping.values()), '该旧称已用作新叫法，请核对合并方向')
    rule = insert(conn, tag_aliases, code=data.code, alias=data.alias,
                  canonical=data.canonical, serial=current_serial(conn) + 1)
    mapping[data.alias] = data.canonical
    switched = {'entrances': 0, 'walk_profiles': 0}
    for row in scan(conn, entrances):
        tags = aliases.normalize_tags(row['tags'], mapping)
        if tags != row['tags']:
            update(conn, entrances, row['code'], tags=tags)
            switched['entrances'] += 1
    for row in scan(conn, walk_profiles):
        avoid, weights = aliases.normalize_profile(row['avoid'], row['weights'], mapping)
        if avoid != row['avoid'] or weights != row['weights']:
            update(conn, walk_profiles, row['code'], avoid=avoid, weights=weights)
            switched['walk_profiles'] += 1
    return {**rule, 'switched': switched}
