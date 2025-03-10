def fix_id(items):
    for item in items:
        item["id"] = str(item["_id"])
    return items


def fix_one_item_id(item):
    item["id"] = str(item["_id"])
    return item
