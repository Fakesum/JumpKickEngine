def main():
    """
        Starting point of the program
    """
    from youtube_promoter.common import (
        settings,
        start_server,
    )
    match settings["type"]:
        case 0:
            from youtube_promoter.reddit import YoutubeViewBot as YoutubeViewBot_Reddit
            [YoutubeViewBot_Reddit().start() for _ in range(settings["dnum"])]
        case 1:
            from youtube_promoter.local import YoutubeViewBot as YoutubeViewBot_Local
            [YoutubeViewBot_Local(settings["local"]["vid_ids"], start_server()).start() for _ in range(settings["dnum"])]
    
    import time
    while True:
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        import sys
        sys.exit(1)