document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("tickerForm");
    const resultDiv = document.getElementById("result");
    const loadingDiv = document.getElementById("loading");
    const chartContainer = document.getElementById("chartContainer");
    let sentimentChart = null;

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const tickers = document.getElementById("tickerInput").value.split(',').map(ticker => ticker.trim());

        // Show loading spinner
        loadingDiv.style.display = "flex";
        resultDiv.innerHTML = "";
        if (sentimentChart) {
            sentimentChart.destroy();
        }
        chartContainer.style.display = "none";

        // Use fetch API to submit the tickers to the Flask backend
        fetch("/results", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ tickers }),
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading spinner
            loadingDiv.style.display = "none";

            // Update the result div with the table
            resultDiv.innerHTML = data.table;

            // Render the chart
            chartContainer.style.display = "block";
            renderChart(data.chart_data);
        })
        .catch((error) => {
            console.error('Error:', error);
            loadingDiv.style.display = "none";
            resultDiv.innerHTML = "<p>Error fetching results. Please try again.</p>";
        });
    });

    function renderChart(chartData) {
        const ctx = document.getElementById('sentimentChart').getContext('2d');
        sentimentChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartData.labels,
                datasets: chartData.datasets
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Mean Polarity Score by Date for Each Ticker'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Mean Polarity Score'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                }
            }
        });
    }
});
