<script>
    // Function to fetch the scraped news
    function fetchNews() {
        fetch("http://127.0.0.1:5000/scrape")
            .then((response) => response.json()) // Parse the JSON response
            .then((data) => {
                alert(data.message); // Alert the message from the response
            })
            .catch((error) => {
                console.error.status("Error Fetching News Data:", error); // Log any errors
            });
    }
</script>

<div>
    <!-- Header Section -->
    <header class="flex justify-center py-7 px-6">
        <h1 class="text-center text-8xl font-mono text-black">
            Welcome to Mai News Scraper
        </h1>
    </header>
    <!-- Main Content Section -->
    <main class="flex flex-grow items-center justify-center py-3 px-3">
        <div class="text-center bg-white rounded-lg shadow-lg p-6">
            <p class="text-center text-xl">
                Here I will scrape all the major news articles from the Atlantic
            </p>
            <button class="mt-6 p-4 bg-indigo-300 rounded-lg" onclick={fetchNews}>
                First, click on this button to start the scrape!
            </button>
            <nav class="mt-6 text-center">
                <a href="/headlines" class="text-indigo-500 hover:text-indigo-700 hover:underline text-lg">
                    Now Access the Headlines Here
                </a>
            </nav>
            <nav class="mt-6 text-center">
                <a href="/summaries" class="text-indigo-500 hover:text-indigo-700 hover:underline text-lg">
                    Now Access the Summaries Here
                </a>
            </nav>
        </div>
    </main>
    <!-- Footer Section -->
    <footer class="py-4 mt-auto">
        <p class="text-center">&copy; 2025 Mai's Website. All rights reserved.</p>
    </footer>
</div>