response_xpath_mapping = {
    "rows": '//div[@id="all"]/div/div',
    "date": './div[1]/div/div[@class="holodule navbar-text"]/text()',
    "schedules": './div[2]/div/div',

    "time": './a/div/div/div[1]/div/div[@class="col-4 col-sm-4 col-md-4 text-left datetime"]/text()[normalize-space()]',
    "red_border": './a[contains(@style, "red")]',

    "link": './a/@href',
    "thumbnail": './a/div/div/div[2]/img/@src',
    "short_name": './a/div/div/div[1]/div/div[@class="col text-right name"]/text()[normalize-space()]',
    "collabs": './a/div/div/div[3]/div/div/img/@src',
}

api_json_path_mapping = {
    "title": 'snippet.title',
    "description": 'snippet.description',
    "scheduledStartTime": 'liveStreamingDetails.scheduledStartTime',
    "actualStartTime": 'liveStreamingDetails.actualStartTime',
    "actualEndTime": 'liveStreamingDetails.actualEndTime',
    "duration": 'contentDetails.duration',
    "channel_id": 'snippet.channelId',
    "name": 'snippet.channelTitle',

    "liveBroadcastContent": 'snippet.liveBroadcastContent',
    "uploadStatus": 'status.uploadStatus',
}

json_item_holo_item_mapping = {
    'schedule.stream.id': 'stream_id',
    'schedule.stream.link': 'stream_link',
    'schedule.stream.title': 'stream_title',
    'schedule.stream.description': 'stream_description',
    'schedule.stream.thumbnail': 'stream_thumbnail',
    'schedule.stream.type': 'stream_type',
    'schedule.stream.state': 'stream_state',
    'schedule.stream.duration': 'stream_duration',
    'schedule.datetime.scheduled_start': 'datetime_scheduled_start',
    'schedule.datetime.actual_start': 'datetime_actual_start',
    'schedule.datetime.actual_end': 'datetime_actual_end',
    'schedule.channel.id': 'channel_id',
    'schedule.channel.name': 'channel_name',
    'schedule.channel.short_name': 'channel_short_name',
    'schedule.channel.collabs': 'channel_collabs',
}

database_item_holo_item_mapping = {
    'stream_id': 'stream_id',
    'stream_link': 'stream_link',
    'stream_title': 'stream_title',
    'stream_description': 'stream_description',
    'stream_thumbnail': 'stream_thumbnail',
    'stream_type': 'stream_type',
    'stream_state': 'stream_state',
    'stream_duration': 'stream_duration',
    'datetime_scheduled_start': 'datetime_scheduled_start',
    'datetime_actual_start': 'datetime_actual_start',
    'datetime_actual_end': 'datetime_actual_end',
    'channel_id': 'channel_id',
    'channel_name': 'channel_name',
    'channel_short_name': 'channel_short_name',
    'channel_collabs': 'channel_collabs',
}

ARCHIVED = "archived"
VIDEO = "video"
LIVE = "live"

ON_ENDED = "on ended"
ON_LIVE = "on live"
ON_SCHEDULED = "on scheduled"

live_content_state_mapping = {
    "none": ON_ENDED,
    "live": ON_LIVE,
    "upcoming": ON_SCHEDULED,
}

DATETIME_FORMAT = r"%Y/%m/%d %H:%M:%S"
