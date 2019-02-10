def value_or_none(dic, key):
    if key in dic:
        return dic[key]
    return None


def value_or_default(dic, key, default):
    if key in dic:
        return dic[key]
    return default
