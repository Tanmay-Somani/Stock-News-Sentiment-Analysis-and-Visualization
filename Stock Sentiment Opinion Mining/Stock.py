from nltk.sentiment.vader import SentimentIntensityAnalyzer
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

sia = SentimentIntensityAnalyzer()

raw_finviz_url = "https://finviz.com/quote.ashx?t="
ticker = input("Enter stock ticker symbol: ").upper()

try:
    url = raw_finviz_url + ticker
    req = Request(url, headers={'user-agent': 'Mozilla/5.0'})
    response = urlopen(req)
    html = BeautifulSoup(response, "html.parser")
    news_table = html.find(id="news-table")

    parsed_list_data = []

    for rows in news_table.findAll("tr"):
        title = rows.a.get_text()
        dtstamp = rows.td.text.strip().split(' ')
        date = dtstamp[0] if len(dtstamp) > 1 else None
        time = dtstamp[-1]

        polarity_score = sia.polarity_scores(title)['compound']

        parsed_list_data.append({
            "Ticker": ticker,
            "Date": date,
            "Time": time,
            "Title": title,
            "Polarity_Score": polarity_score
        })

    df = pd.DataFrame(parsed_list_data, columns=['Ticker', 'Date', 'Time', 'Title', 'Polarity_Score'])
    def parse_date(date_str):
        if pd.isna(date_str):
            return None
        if date_str == "Today":
            return pd.Timestamp.now().date()
        elif date_str == "Yesterday":
            return (pd.Timestamp.now() - pd.Timedelta(days=1)).date()
        else:
            return pd.to_datetime(date_str, errors='coerce').date()

    df["Date"] = df["Date"].apply(parse_date)
    df.to_csv("Data.csv", index=False)

    mean_df = df.groupby(['Ticker', 'Date'])['Polarity_Score'].mean().unstack()
    mean_df.transpose().plot(kind='bar', figsize=(10, 8))
    plt.title('Mean Polarity Score by Date for Each Ticker')
    plt.ylabel('Mean Polarity Score')
    plt.xlabel('Date')
    plt.legend(title='Ticker')
    plt.show()


    print(mean_df)
except HTTPError as e:
    print("Can't find the URL:", e)
