from youtube_promoter.common import (
    settings,
    start_server,
)

def get_video_ids():
    if settings["local"]["locator"] == "video_ids":
        return settings["local"]["video_ids"]
    
    import scrapetube
    return [video["videoId"] for video in scrapetube.get_channel(settings["local"]["channel_id"], content_type = "shorts")] 

def main():
    """
        Starting point of the program
    """
    match settings["type"]:
        case 0:
            from youtube_promoter.reddit import YoutubeViewBot as YoutubeViewBot_Reddit
            [YoutubeViewBot_Reddit().start() for _ in range(settings["dnum"])]
        case 1:
            from youtube_promoter.local import YoutubeViewBot as YoutubeViewBot_Local
            port = start_server(get_video_ids())
            [YoutubeViewBot_Local(port).start() for _ in range(settings["dnum"])]
    
    import time
    while True:
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        import sys
        sys.exit(1)