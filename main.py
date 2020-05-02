from urllib.request import urlopen
from urllib.parse import urljoin, urldefrag
from urllib.error import HTTPError
from re import search, IGNORECASE, MULTILINE
from bs4 import BeautifulSoup
from sys import stderr

def get_soup(url):
    try:
        html = urlopen(url).read().decode('utf-8')
        return BeautifulSoup(html, 'html.parser')
    except HTTPError as e:
        stderr.write(e.reason)
    except:
        stderr.write('Error')

def get_links(soup):
    atags = soup.find_all('a', href=True)
    hrefs = [urljoin(wiki_url, l['href']) for l in atags]
    defraged = [urldefrag(h)[0] for h in hrefs]
    return [h for h in defraged if search(fr'^{wiki_url}', h)]

def run(search_term, url, max_iter):
    it = 0
    queue = [url]
    visited = set()
    while(len(queue)):
        it += 1
        if (it == max_iter):
            return
        current = queue.pop(0)
        print(f'Current: {current}')
        soup = get_soup(current)
        if not soup:
            continue
        has_found = search(fr'^.* {search_term} .*$', soup.text, IGNORECASE | MULTILINE)
        if has_found and current not in found:
            found.add((current, has_found.group(0)))
        links = list(set(get_links(soup)))
        not_visited_links = [l for l in links if l not in visited]
        not_in_queue = [l for l in not_visited_links if l not in queue]
        queue.extend(not_in_queue)
        visited.update(not_visited_links)

search_lang = input('Provide language\n')
search_term = input('Provide searched term\n')
start_search = input('Provide start search\n')
iters = input('Provide number of iterations\n')

language = search_lang or 'en'
wiki_url = f'https://{language}.wikipedia.org/wiki/'
found = set()

run(search_term, f'{wiki_url}{start_search}', int(iters) or 20)
print('\n\n'.join(f'{x[0]}\n{x[1]}\n' for x in found))
