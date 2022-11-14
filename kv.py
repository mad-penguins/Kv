from bs4 import BeautifulSoup


class Kv:
    """docstring for Kv"""
    def __init__(self, siteaddress, filename=None):
        self.kv_url = siteaddress
        self.filename = filename

    def getSoupFromFile(self):
        with open(self.filename, 'r') as f:
            html_text = f.read()

        soup = BeautifulSoup(html_text, 'lxml')

        return soup

    def getPostsFromSoup(self, soup):
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
        d['id'] = _id

        _date = p_head.find("a", class_="wi_date").text
        d['head']['date'] = _date

        _link = p_head.find("a", class_="wi_date").get("href")
        d['head']['link'] = self.kv_url + _link

        p_body = post_html.find("div", class_='wi_body')

        _text = p_body.find("div", class_='pi_text')
        if _text is not None:
            if "wi_body" in _text.parent.get('class'):
                d['body']['text'] = _text.text

        if _copy is not None:
            p_orig = post_html.find('div', class_='pic_body_wrap')

            d['body']['orig_head'] = {}
            d['body']['orig_body'] = {}

            _orig_author = p_orig.find("a", class_='pi_author').text
            d['body']['orig_head']['author'] = _orig_author

            _orig_date = p_orig.find("a", class_='pic_desc_a').text
            d['body']['orig_head']['date'] = _orig_date

            _orig_link = p_orig.find("a", class_='pic_desc_a').get("href")
            d['body']['orig_head']['link'] = self.kv_url + _orig_link

            _orig_text = p_orig.find("div", class_='pi_text')
            d['body']['orig_body']['text'] = _orig_text.text

        return d

    def proccesFile(self):
        if self.filename is None:
            return

        soup = self.getSoupFromFile()

        response = []

        for post in self.getPostsFromSoup(soup):
            post_data = self.parsePost(post)
            response.append(post_data)

        return response

    def process(self, html_text):
        soup = BeautifulSoup(html_text, 'lxml')
        del html_text

        response = []

        for post in self.getPostsFromSoup(soup):
            post_data = self.parsePost(post)
            response.append(post_data)

        return response



