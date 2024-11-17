from .constant import (
    json_item_holo_item_mapping,
    database_item_holo_item_mapping
)

from .items import (
    HoloSchedulesJSONItem,
    HoloSchedulesDatabaseItem
)

def convert_item(cls, item):
    if cls is HoloSchedulesJSONItem:
        return _convert_new_item(cls(), item, json_item_holo_item_mapping)
    if cls is HoloSchedulesDatabaseItem:
        return _convert_new_item(cls(), item, database_item_holo_item_mapping)

def _convert_new_item(new_item, item, mapping):
    for key, value in mapping.items():
        value = item.get(value, None)
        if value is None:
            continue
        keys = key.split('.')
        current_dict = new_item

        for key in keys[:-1]:
            current_dict = current_dict.setdefault(key, {})
        current_dict[keys[-1]] = ",".join(value) if isinstance(value, list) else value

    return new_item
