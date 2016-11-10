import re

if __name__ == '__main__':

    regex_list = [
        r"(?:@[\w]+)", #mentions 
        r"(?:#[\w]+)", #hash-tags
        r"&#\d+;", #unicode (emoticons and othes symbols)
        r"\S+&#\d+;$", # sentence ending with ellipsis
        r"http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+", #urls
        r"&\w+;", # html entities
        r"(?:[$]?(?:\d+,?)+(?:\.?\d+)?)[a-zA-Z]*", #numbers
        r"\w+&#\d+;\w+", # words with accents
        # r"(?:[a-zA-Z][a-zA-Z'\-_]+[a-zA-Z]*)", # words
        r"(?:\w[\w'\-_]+\w*)", # words
        r"[:=;][oO\-]?[D\)\]\(\]/\\OpP]", #emoticons
        r"[!?.]+", #extra punc
        r"(?:\S)" #other characters
    ]

    fp = open("./tweets.en.txt", 'r')
    for line in fp:
    	line = line.decode('utf-8').encode("ascii", "xmlcharrefreplace")
    	print re.findall('|'.join(regex_list), line)