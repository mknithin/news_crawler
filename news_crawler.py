import requests
from lxml import html


class NewsCrawler:
    def __init__(self, host, starting_url, depth):
        self.host = host
        self.starting_url = starting_url
        self.depth = depth
        self.sections = []
        self.articles = []

    def crawl(self):
        section = self.get_section_from_link(self.starting_url)
        self.sections.extend(section)
        print self.sections
        article = self.get_articles_from_link(self.host, self.sections)
        self.articles.extend(article)
        obj = self.scrap_article_from_link(self.host, self.articles)
        print obj
        return

    def get_section_from_link(self, link):
        headline_page = requests.get(link)
        tree = html.fromstring(headline_page.text)
        section_links = tree.xpath('//div[@class = "col-md-12 col-sm-12 col-xs-12 section_links"]//*/a/@href')[1:5]
        # print section_links
        return section_links

    def get_articles_from_link(self, host, sections_link):
        articles_link = []
        for link in sections_link:
            articles_page = requests.get(host+link)
            tree = html.fromstring(articles_page.text)
            links = tree.xpath('//div[@class = "col-md-12 col-sm-12 col-xs-12"]//*/a/@href')
            articles_link.extend(list(set(links)))
        print articles_link
        return articles_link

    def scrap_article_from_link(self, host, article_link):
        for link in article_link:
            print host+link
            if link == "#" or None:
                continue
            article_page = requests.get(host+link)
            tree = html.fromstring(article_page.text)
            a_name = tree.xpath('//h1[@class = "title common_text"]/text()')
            a_description = tree.xpath('//div[@class = "col-md-12 col-sm-12 col-xs-12"]//*/p/text()')
            if a_name is not None:
                print a_name[0]
            if a_description is not None:
                for des in a_description:
                    print des
        art = Article(a_name, a_description)

        return art

class Article:
    def __init__(self, article_name, article_description):
        self.article_name = article_name
        self.article_description = article_description
        # self.article_comments = article_comments
        return


host = "http://www.mathrubhumi.com"
start_page = "http://www.mathrubhumi.com/news"
crawler = NewsCrawler(host, start_page, 0)
crawler.crawl()
