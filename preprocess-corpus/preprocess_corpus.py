rawfile = open('phrased.txt', 'r', encoding='utf8')
textfile = open('text.txt', 'w', encoding='utf8')
articles = []

for article in rawfile.read().splitlines():
    if article not in articles:
        articles.append(article)
        textfile.write(article + '\n')
