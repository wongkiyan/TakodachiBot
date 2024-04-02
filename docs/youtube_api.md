# Parts list values
- id: 視頻的唯一標識符，通常是一個字符串。
- contentDetails: 視頻的內容詳細資訊，例如視頻的長度、視頻視圖的數量、顯示影片是否可使用字幕的指示等。
- liveStreamingDetails: 視頻的直播流詳細資訊，如果視頻是直播視頻的話。包括直播的開始時間、預定的結束時間等。
- localizations: 視頻的本地化語言資訊，包括標題、描述等的不同語言版本。
- player: 視頻的嵌入播放器設定，可以用於在網站上嵌入播放器。
- recordingDetails: 視頻的錄製詳細資訊，如果是由鏡頭錄製的話。包括錄製的日期、地點等。
- statistics: 視頻的統計數據，例如視頻的喜歡數、不喜歡數、評論數等。
- status: 視頻的狀態信息，包括視頻的隱私設置、是否被封鎖、是否有版權等。
- snippet: 視頻的摘要資訊，包括標題、描述、標籤等。
- topicDetails: 視頻的主題詳細資訊，如果視頻屬於特定主題的話。
- fileDetails(video's owner): 視頻文件的詳細資訊，例如視頻的文件類型、文件大小、文件的最後修改日期等。
- processingDetails(video's owner): 視頻的處理進度資訊，包括視頻的處理狀態、處理進度等。
- suggestions(video's owner): 視頻的建議建議，包括其他相關的視頻。

# useful value
- items (list)
- items[] > ['snippet'] > ['channelId']
- items[] > ['snippet'] > ['channelTitle']
- items[] > ['snippet'] > ['title']
- items[] > ['snippet'] > ['description']
- items[] > ['snippet'] > ['thumbnails']
- items[] > ['snippet'] > ['liveBroadcastContent'] ("none" = on ended, "live" = on live, "upcoming" = on scheduled)

- items[] > ['status'] > ['uploadStatus'] ("processed" = on archived / on scheduled video, "uploaded" = on live / on scheduled live)
- items[] > ['contentDetails'] > ['duration'] ("PT#H#M#S" = 時間範圍 小時 分鐘 秒數, "P0D" = on live)

- items[] > ['liveStreamingDetails'] > ['scheduledStartTime'] 
- 
- items[] > ['liveStreamingDetails'] > ['actualStartTime'] (on live started)
- items[] > ['liveStreamingDetails'] > ['concurrentViewers'] (if on live)
- items[] > ['liveStreamingDetails'] > ['activeLiveChatId'] (if on live / on scheduled)
- 
- items[] > ['liveStreamingDetails'] > ['actualEndTime'] (on live ended)

items: [] (len = number of id input)
- kind: ""
- etag: ""
- id: ""
- snippet
  - publishedAt: ""
  - channelId: ""
  - channelTitle: ""
  - title: ""
  - description: ""
  - thumbnails
    - default:{"width": 120, "height": 90, "url": f"https://i.ytimg.com/vi/{id}/default.jpg"},
    - medium:{"width": 320, "height": 180, "url": f"https://i.ytimg.com/vi/{id}/mqdefault.jpg"},
    - high:{"width": 480, "height": 360, "url": f"https://i.ytimg.com/vi/{id}/hqdefault.jpg"},
    - standard:{"width": 640, "height": 480, "url": f"https://i.ytimg.com/vi/{id}/sddefault.jpg"},
    - maxres:{"width": 1280, "height": 720, "url": f"https://i.ytimg.com/vi/{id}/maxresdefault.jpg"}
  - tags: []
  - categoryId: ""
  - liveBroadcastContent: ""
  - localized
    - title: ""
    - description: ""
  - defaultAudioLanguage: ""
- contentDetails
  - duration: ""
  - dimension: ""
  - definition: ""
  - caption: ""
  - licensedContent: bool
  - contentRating: {}
  - projection: ""
- status
  - uploadStatus: ""
  - privacyStatus: ""
  - license: ""
  - embeddable: bool
  - publicStatsViewable: bool
  - madeForKids: bool
- statistics
  - viewCount: ""
  - likeCount: ""
  - favoriteCount: "" (always 0)
  - commentCount: ""
- player
  - embedHtml
- topicDetails (may not exists)
  - topicCategories: []
- recordingDetails
- liveStreamingDetails
  - actualStartTime: "" (on live started)
  - actualEndTime: "" (on live ended)
  - scheduledStartTime: "" (always exists if not non stop stream)
  - concurrentViewers: "" (if on live)
  - activeLiveChatId: "" (if on live / on scheduled)

# Reference
https://developers.google.com/youtube/v3/docs/videos?hl=zh-tw