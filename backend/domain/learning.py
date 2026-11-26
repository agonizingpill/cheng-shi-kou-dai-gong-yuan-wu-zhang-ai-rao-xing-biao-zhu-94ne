from sklearn.preprocessing import MultiLabelBinarizer

from domain.tag_aliases import normalize_profile, normalize_tags


def calculate(data):
    profile, entrances = data['profile'], data['entrances']
    mapping = data.get('aliases') or {}
    avoid, weights = normalize_profile(profile['avoid'], profile['weights'], mapping)
    total = sum(weights.values())
    if not avoid or total <= 0:
        raise ValueError('偏好卡没有有效的避让权重')
    tags = [normalize_tags(row['tags'], mapping) for row in entrances]
    mlb = MultiLabelBinarizer()
    vectors = mlb.fit_transform([avoid] + tags)
    scale = [weights.get(name, 0) for name in mlb.classes_]
    ranked = []
    for record, names, bits in zip(entrances, tags, vectors[1:]):
        overlap = sum(weight * int(bit) for weight, bit in zip(scale, bits))
        deductions = [{'item': name, 'weight': weights[name]} for name in avoid if name in names]
        ranked.append({'entry': record['code'], 'score': round(1 - overlap / total, 4),
                       'ramp': record['ramp'], 'deductions': deductions})
    ranked.sort(key=lambda r: (-r['score'], not r['ramp'], r['entry']))
    return {'classes': mlb.classes_.tolist(), 'ranked': ranked}
