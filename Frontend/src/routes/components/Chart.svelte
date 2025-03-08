<script>
    import { onMount } from "svelte";
    import { Chart, CategoryScale, LinearScale, BarController, BarElement, Title, Tooltip, Legend } from "chart.js";
    import { API_BASE_URL } from "../../config.js";

    let headlinesData = [];
    let chart = null;

    // Register necessary components for the chart
    Chart.register(CategoryScale, LinearScale, BarController, BarElement, Title, Tooltip, Legend);

    onMount(async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/headlines`);
            const data = await response.json();
            console.log("Fetched Data:", data);  // Debugging statement
            headlinesData = data;

            // Initialize counters for the keywords
            let trumpCount = 0;
            let americaCount = 0;
            let dogeCount = 0;

            // Count occurrences of each keyword in the headlines
            headlinesData.forEach((article) => {
                if (article.headline.includes("Trump")) trumpCount++;
                if (article.headline.includes("America")) americaCount++;
                if (article.headline.toLowerCase().includes("doge")) dogeCount++;
            });

            // Log the counts for debugging
            console.log("Trump Count:", trumpCount);
            console.log("America Count:", americaCount);
            console.log("Doge Count:", dogeCount);

            // Prepare the chart data with the counts
            const chartData = {
                labels: ["Trump", "America", "Doge"],
                datasets: [
                    {
                        label: "Article Count",
                        data: [trumpCount, americaCount, dogeCount],
                        backgroundColor: [
                            "rgba(255, 99, 132, 0.2)",
                            "rgba(54, 162, 235, 0.2)",
                            "rgba(255, 206, 86, 0.2)",
                        ],
                        borderColor: [
                            "rgba(255, 99, 132, 1)",
                            "rgba(54, 162, 235, 1)",
                            "rgba(255, 206, 86, 1)",
                        ],
                        borderWidth: 1,
                    },
                ],
            };

            // Create the chart
            const ctx = document.getElementById("headlineChart").getContext("2d");
            chart = new Chart(ctx, {
                type: "bar",
                data: chartData,
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    });
</script>

<h1>News Headlines Visualization</h1>
<canvas id="headlineChart"></canvas>

<style>
    #headlineChart {
        max-width: 600px;
        max-height: 400px;
        width: 100%;
        height: 100%;
    }
</style>
