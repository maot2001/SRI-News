from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAJE = "english"
def summarize(text:str, SENTENCES_COUNT=5):
    """Parse the input string and using sumy library summrizes the text 

    Args:
        text (str): the text to summarize
        SENTENCES_COUNT (int): in how many sentences do you want to summarize the text. Defaults to 5

    Returns:
        srt: SENTENCES_COUNT within a single string.
    """
    
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAJE))
    stemmer = Stemmer(LANGUAJE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAJE)
    res = ""
    sentences = summarizer(parser.document, SENTENCES_COUNT)
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        res = res + sentence._text    
    return res
