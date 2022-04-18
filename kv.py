from bs4 import BeautifulSoup


class Kv:
    """docstring for Kv"""
    def __init__(self, filename):
        self.kv_url = 'https://m.vk.com'

        self.filename = filename

    def getSoup(self):
        with open(self.filename, 'r') as f:
            html_text = f.read()

        soup = BeautifulSoup(html_text, 'lxml')

        return soup

    def getPostsBySoup(self, soup):
        posts_div_html = soup.find("div", attrs={ "class": "wall_posts"})
        posts_html = posts_div_html.find_all(class_="wall_item")

        return posts_html

    def parsePost(self, post_html):
        d = {}
        d['head'] = {}
        d['body'] = {}

        _copy = post_html.get('data-copy')
        if _copy is None:
            d['head']["copy"] = False
        else:
            d['head']["copy"] = True

        p_head = post_html.find("div", class_='wi_head')

        _author = p_head.find("a", class_="pi_author").text
        d['head']['author'] = _author

        _id = p_head.find("a", class_="pi_author").get("data-post-id")
        d['head']['id'] = _id

        _date = p_head.find("a", class_="wi_date").text
        d['head']['date'] = _date

        _link = p_head.find("a", class_="wi_date").get("href")
        d['head']['link'] = self.kv_url + _link

        return d



