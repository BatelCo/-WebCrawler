import requests
from lxml import html
import playerPageRank


def updatePriority(url, priority_list):
    for reference in priority_list:
        if reference[0] == url:
            reference[1] += 1
            return


def get_top_url(priority_list, visited):
    max_url = None
    max_priority = 0
    for pair in priority_list:
        if pair[0] not in visited:
            if pair[1] > max_priority:
                max_priority = pair[1]
                max_url = pair[0]
    return max_url


def address_in_list(address, priority_list):
    for pair in priority_list:
        if pair[0] == address:
            return True
    return False


def crawl_until_limit(url, xpaths, url_counter, priority_list, src_to_dest, url_limit, visited):
    page = requests.get(url)
    doc = html.fromstring(page.content)
    visited.add(url)
    for xpath in xpaths:
        for address in doc.xpath(xpath):
            if "http://" not in address:
                address = "https://en.wikipedia.org" + address
                print(address)
            if not address_in_list(address, priority_list):
                priority_list.append([address, 1])
                src_to_dest.append([url, address])
                url_counter += 1
            else:
                # update url's priority
                updatePriority(address, priority_list)
    if url_counter < url_limit:
        top_url = get_top_url(priority_list, visited)
        return crawl_until_limit(top_url, xpaths, url_counter, priority_list, src_to_dest, url_limit, visited)
    else:
        return src_to_dest


def crawl(url, xpaths):
    return crawl_until_limit(url, xpaths, 0, priority_list=[], src_to_dest=[], url_limit=100, visited=set())


if __name__ == '__main__':
    url = "https://en.wikipedia.org/wiki/Andy_Ram"
    xPaths = []
    xPaths.append("//a[contains(text(),'Nathalie')]/@href")
    xPaths.append(
        "//table[contains(.,'Partner') or contains(.,'with') or contains(.,'lost to') or contains(.,'defeated') or contains(.,'seed') or contains(.,'world #') or contains(.,'over') or contains(.,'beat')]/tbody/tr/td/span[@class='flagicon']/following-sibling::a/@href")
    links = crawl(url, xPaths)

    with open("outputs.txt", 'w') as file:
        for link in links:
            file.write(link[0] + " -> " + link[1] + '\n')
            print(link[0] + " -> " + link[1] + '\n')
        file.write("\n\n")
        # [url] -> (first_hits, second_hits)
        links_to_hits = playerPageRank.playerPagerank(links)
        max_hits = 0
        max = None
        for thing in links_to_hits.keys():
            if links_to_hits[thing][0] > max_hits:
                max_hits = links_to_hits[thing][0]
                max = thing
            file.write(thing + " -> " + str(links_to_hits[thing][0]) + ", " + str(links_to_hits[thing][1]) + '\n')
            print(thing + " -> " + str(links_to_hits[thing][0]) + ", " + str(links_to_hits[thing][1]) + '\n')
        file.write("\n\nmax: " + max + " -> " + str(links_to_hits[max][0]) + ", " + str(links_to_hits[max][1]) + '\n')
        print("\n\nmax: " + max + " -> " + str(links_to_hits[max][0]) + ", " + str(links_to_hits[max][1]) + '\n')
