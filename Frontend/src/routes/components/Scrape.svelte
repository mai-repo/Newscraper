<script>
    import Articles from "./Articles.svelte";
    import { userData } from "./store.ts";

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
    <header class="flex flex-col justify-center py-7 px-6">
        <h1 class="mb-6 text-center text-6xl font-mono text-black">
            Welcome to Mai News Scraper
        </h1>
        <nav-bar class="flex justify-center py-5">
            <p class="text-4xl"> Hello, {$userData.name}</p>
        </nav-bar>
    </header>
    <Articles/>
    <!-- Footer Section -->
    <footer class="py-4 mt-auto">
        <p class="text-center">&copy; 2025 Mai's Website. All rights reserved.</p>
    </footer>
</div>