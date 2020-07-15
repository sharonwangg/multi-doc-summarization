library(readr)
news_csv = read_csv("news.csv")
articles = news_csv$text
write.table(articles, file = "articles.txt", row.names = FALSE, col.names = FALSE)
