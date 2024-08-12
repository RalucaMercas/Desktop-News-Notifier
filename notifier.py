import time
import webbrowser
from topnews import topStories
from win10toast_click import ToastNotifier

newsitems = topStories()

def openLink():
    try:
        webbrowser.open(link)
    except Exception as e:
        print(f"Cannot open the link: {e}")
i = 0
toast = ToastNotifier()
for newsitem in newsitems:
    link = newsitem['link']
    i += 1
    toast.show_toast(newsitem['pubDate'], newsitem['title'], duration=20, callback_on_click=openLink)
    time.sleep(15)

