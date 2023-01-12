
import feedparser
from datetime import datetime
from datetime import time

class OktaTrustClient:

    def __init__(self):
        self.feeds_url = feedparser.parse("https://feeds.feedburner.com/OktaTrustRSS")

    def get_okta_trust_event(self):
            print("call receieve")
            if self.feeds_url:
                current_time_stamp = datetime.now().timestamp()
                
                trust_events = {'updated': self.feeds_url['updated'], 'okta_events': list()}
                for entry in self.feeds_url["entries"]:
                    
                    updated = entry["updated"]
                    rssdate = datetime.strptime(updated, '%Y-%m-%dT%H:%M:%S.%f%z')
                    rss_timestamp = rssdate.timestamp()

                    if (((current_time_stamp - rss_timestamp) / 60) <= 5000 ):
                        trust_event = {'title': entry['title'],
                                    'updated': entry['updated'],
                                    'links': list(),
                                    'contents': list()}

                        #include feed in digest, otherwise ignore
                        if entry["links"]:
                            for link in entry["links"]:
                                trust_event['links'].append({'href': link['href']})
                                #TODO: Implement scraping of the detailed status from the href

                        if entry["content"]:
                            for content in entry["content"]:
                                trust_event['contents'].append({'value': content['value']})
                        trust_events['okta_events'].append(trust_event)
                    else:
                        break
                return trust_events

if __name__ == '__main__':

    okta_client = OktaTrustClient()
    content = okta_client.get_okta_trust_event()

    print(content)
