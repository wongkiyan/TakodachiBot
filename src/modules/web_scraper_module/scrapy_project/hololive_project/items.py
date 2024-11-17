# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class HololiveProjectItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HoloSchedulesItem(Item):
    # Stream fields
    stream_id = Field()
    stream_link = Field()
    stream_title = Field()
    stream_description = Field()
    stream_thumbnail = Field()
    stream_type = Field()
    stream_state = Field()
    stream_duration = Field()
    # Datetime fields
    datetime_scheduled_start = Field()
    datetime_actual_start = Field()
    datetime_actual_end = Field()

    # Channel fields
    channel_id = Field()
    channel_name = Field()
    channel_short_name = Field()
    channel_collabs = Field()

class HoloSchedulesJSONItem(Item):
    schedule = Field()

    schedule['stream'] = Field()
    schedule['datetime'] = Field()
    schedule['channel'] = Field()

    schedule['stream']['id'] = Field()
    schedule['stream']['link'] = Field()
    schedule['stream']['title'] = Field()
    schedule['stream']['description'] = Field()
    schedule['stream']['thumbnail'] = Field()
    schedule['stream']['type'] = Field()
    schedule['stream']['state'] = Field()
    schedule['stream']['duration'] = Field()

    schedule['datetime']['scheduled_start'] = Field()
    schedule['datetime']['stream_start'] = Field()
    schedule['datetime']['stream_end'] = Field()

    schedule['channel']['id'] = Field()
    schedule['channel']['name'] = Field()
    schedule['channel']['short_name'] = Field()
    schedule['channel']['collabs'] = Field()

class HoloSchedulesDatabaseItem(Item):
    # Stream fields
    stream_id = Field()
    stream_link = Field()
    stream_title = Field()
    stream_description = Field()
    stream_thumbnail = Field()
    stream_type = Field()
    stream_state = Field()
    stream_duration = Field()

    # Datetime fields
    datetime_scheduled_start = Field()
    datetime_actual_start = Field()
    datetime_actual_end = Field()

    # Channel fields
    channel_id = Field()
    channel_name = Field()
    channel_short_name = Field()
    channel_collabs = Field()

    old_stream_title = Field()
    old_datetime_scheduled_start = Field()