from io import StringIO


class JsChartClass:
    def __init__(self, data, accommodation):
        self.data = data
        self.accommodation = accommodation
        self.content = self._generate_chart_page()

    def _generate_chart_page(self) -> str:
        """
        Generate the chart page HTML content dynamically using StringIO.

        Returns:
            str: The generated HTML content as a string.
        """
        dict_data = self.data.to_dict(orient="list")

        # Use StringIO to construct the HTML content
        s = StringIO()

        # Write HTML content
        s.write(
            """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dynamic Bar Chart</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin: 0;
                    padding: 20px;
                }
                canvas {
                    width: 60% !important;  /* Adjust width */
                    height: 400px !important;  /* Adjust height */
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Total Accommodation by Parish</h1>
            <canvas id="barChart"></canvas>
            <script>
                // Dynamically injected JSON data from Python
                const parishData = """
        )
        s.write(str(dict_data))
        s.write(
            """;

                // Function to create and render the Chart.js bar chart
                function createChart() {
                    const ctx = document.getElementById('barChart').getContext('2d');
                    const chart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: parishData.parish,
                            datasets: [{
                                label: 'Total Accommodations',
                                data: parishData."""
        )
        s.write(self.accommodation)
        s.write(
            """,
                                backgroundColor: 'rgba(0, 128, 0, 1)',  /* Solid metallic green */
                                borderColor: 'rgba(0, 128, 0, 1)',  /* Solid metallic green */
                                borderWidth: 2
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: { position: 'top' },
                                title: { display: true, text: 'Total Accommodation by Parish' }
                            },
                            scales: {
                                y: { beginAtZero: true }
                            }
                        }
                    });
                }

                // Call the function to create the chart
                createChart();
            </script>
        </body>
        </html>
        """
        )

        # Get the complete content as a string
        return s.getvalue()


def expose_js_chart(chart_element: JsChartClass) -> str:
    """
    Exposes the generated chart page to Taipy as HTML content.

    Args:
        chart_element (JsChartClass): The chart object containing the HTML content.

    Returns:
        str: The HTML content for rendering in Taipy.
    """
    return chart_element.content
