from flask import Flask, render_template, request, jsonify
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import asyncio
import aiohttp

app = Flask(__name__)
sia = SentimentIntensityAnalyzer()

async def fetch_ticker_data(ticker):
    raw_finviz_url = "https://finviz.com/quote.ashx?t="
    ticker = ticker.upper()
    url = raw_finviz_url + ticker

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return {"error": f"Can't find the URL for {ticker}"}
            html = await response.text()
            news_table = BeautifulSoup(html, "html.parser").find(id="news-table")
            if news_table is None:
                return {"error": f"News table not found for {ticker}"}
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
            return parsed_list_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
async def results():
    tickers = request.json['tickers']

    tasks = [fetch_ticker_data(ticker) for ticker in tickers]
    all_data = await asyncio.gather(*tasks)

    # Flatten the results and filter out errors
    combined_data = []
    for data in all_data:
        if isinstance(data, list):  # If the fetched data is a list, append it
            combined_data.extend(data)
        elif isinstance(data, dict) and 'error' in data:  # If there's an error, handle it accordingly
            return jsonify({"error": data['error']}), 404

    if not combined_data:
        return jsonify({"error": "No valid data found"}), 404

    df = pd.DataFrame(combined_data, columns=['Ticker', 'Date', 'Time', 'Title', 'Polarity_Score'])

    # Calculate aggregated values (mean polarity score for each ticker)
    aggregated_df = df.groupby('Ticker')['Polarity_Score'].mean().reset_index()
    aggregated_df['Mean_Polarity_Score'] = aggregated_df['Polarity_Score'].round(4)
    aggregated_df = aggregated_df.drop('Polarity_Score', axis=1)

    # Format the aggregated table to HTML
    aggregated_table = aggregated_df.to_html(classes='data', index=False)

    # Prepare chart data
    mean_df = df.groupby(['Ticker', 'Date'])['Polarity_Score'].mean().unstack()
    chart_data = {
        'labels': mean_df.index.tolist(),
        'datasets': [
            {
                'label': ticker,
                'data': mean_df[ticker].tolist(),
                'backgroundColor': f'rgba({hash(ticker) % 256}, {(hash(ticker) * 2) % 256}, {(hash(ticker) * 3) % 256}, 0.7)'
            } for ticker in mean_df.columns
        ]
    }

    return jsonify({
        'table': aggregated_table,
        'chart_data': chart_data
    })

if __name__ == '__main__':
    app.run(debug=True)
