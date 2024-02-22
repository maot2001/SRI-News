from newspaper import Article

def get_info_url(url):
   """Get the title, authors and content of the entry link

    Args:
        url (str): the url to get the information

    Returns:
        (str, str, list(str)): article.title, article.text, article.authors
   """
   try:
      article = Article(url)
      article.download()
      article.parse()
      return article.title, article.text, article.authors
   except:
      return Exception