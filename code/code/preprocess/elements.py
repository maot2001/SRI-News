#from . 
import news_url

class Docs:
    def __init__(self, url, title=None, text=None, authors=None):
        if not title:
            try:
                self.title, self.text, self.authors = news_url.get_info_url(url)
            except:
                return Exception
        else:
            self.title = title
            self.text = text
            self.authors = authors
        self.url = url

    def to_dict(self):
        return {
            'title': self.title,
            'authors': self.authors,
            'url' : self.url,
            'text': self.text
        }

class Words:
    def __init__(self, word, idf):
        self.word = word
        self.docs = []
        self.idf = idf

    def to_dict(self):
        return {
            'word': self.word,
            'idf' : self.idf,
            'docs': [ {
                'id': doc[0],
                'tf-idf': doc[1]
            } for doc in self.docs]
        }