# Stock Sentiment Analysis

## Description

This project is a web application that performs sentiment analysis on stock market news. It allows users to input stock ticker symbols and retrieve sentiment scores based on recent news articles. The application uses natural language processing techniques to analyze the sentiment of news headlines and presents the results in an easy-to-understand format.

## Features

- Input multiple stock ticker symbols
- Asynchronous fetching of stock news data
- Sentiment analysis using NLTK's VADER sentiment analyzer
- Interactive data visualization with Chart.js
- Responsive design for various screen sizes

## Technologies Used

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Data Scraping: BeautifulSoup4
- Sentiment Analysis: NLTK (Natural Language Toolkit)
- Data Visualization: Chart.js
- Asynchronous HTTP Requests: aiohttp

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/stock-sentiment-analysis.git
   cd stock-sentiment-analysis
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Download the NLTK VADER lexicon:
   ```
   python -c "import nltk; nltk.download('vader_lexicon')"
   ```

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Enter stock ticker symbols separated by commas (e.g., AAPL, GOOGL, MSFT)

4. Click the "Analyze Sentiment" button to view the results

## Project Structure

```
stock-sentiment-analysis/
│
├── app.py                # Flask application
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   └── index.html        # Main page
├── static/               # Static files (CSS, JS)
│   ├── style.css         # CSS styles
│   └── script.js         # JavaScript for frontend functionality
└── README.md             # Project documentation
```

## Contributing

Contributions to improve the project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request


## Acknowledgments

- [NLTK](https://www.nltk.org/) for providing the VADER sentiment analysis tool
- [Chart.js](https://www.chartjs.org/) for the interactive data visualization
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping capabilities



Project Link: [https://github.com/tanmay-somani/stock-sentiment-analysis](https://github.com/tanmay-somani/stock-sentiment-analysis)
