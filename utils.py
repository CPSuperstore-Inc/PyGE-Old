from PyGE.exceptions import MissingMandatoryArguementException

def value_or_none(dic, key):
    if key in dic:
        return dic[key]
    return None


def value_or_default(dic, key, default):
    if key in dic:
        return dic[key]
    return default


def get_mandatory_value(dic, key):
    if key in dic:
        return dic[key]
    raise MissingMandatoryArguementException("The Key '{}' Was Expected, But Not Defined".format(key))