import time
from plyer import notification
from topnews import topStories

newsitems = topStories()

for newsitem in newsitems:
    notification.notify(
        title=newsitem['pubDate'],
        message=newsitem['title'],
        app_icon=None,
        timeout=20
    )

    time.sleep(15)
