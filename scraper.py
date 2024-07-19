from webpage import Webpage

from queue import Queue

class Scraper:
    @staticmethod
    def scrape_from_link(link, max_items=20):
        link_queue = Queue()
        link_queue.put(link)
        webpages = []
        passed_links={
            link: True
        } # I assume this is a map and has search complexity of O(log N) or O(1)


        while link_queue.qsize() > 0 and len(webpages) < max_items:
            link = link_queue.get()
            try: # In case page is invalid, skip it
                item = Webpage(link)
                connects = item.get_connects()
            except:
                #print(f"INVALID LINK: {link}")
                continue
            webpages.append(item)

            for x in connects:
                if x in passed_links:
                    continue
                passed_links[x] = True
                link_queue.put(x)
        
        return webpages 
                