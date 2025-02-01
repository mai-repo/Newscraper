<script>
    import AddFavorite from "./AddFavorite.svelte";
    import { news, articlesData } from "./store.ts";

    let searchInput = '';

    // Function to scrape news articles from the backend
    async function scrapeNews() {
        try {
            const response = await fetch('http://127.0.0.1:5000/scrape');
            const data = await response.json();
            articlesData.set(data); // Update the articlesData store with the scraped data
        } catch (error) {
            console.error('Error scraping news:', error);
        }
    }

    // Function to fetch news articles from the backend
    async function fetchNews() {
        try {
            const response = await fetch('http://127.0.0.1:5000/news');
            const data = await response.json();
            news.set(data); // Update the news store with the fetched data
        } catch (error) {
            console.log('Error fetching news:', error);
        }
    }

    // Function to filter by Headline Title
    function filterHeadlines() {
        return $news.filter(article => article.headline.toLowerCase().includes(searchInput.toLowerCase()));
    }
</script>

<main class="flex flex-col justify-center items-center py-5 gap-3">
    <h1 class="text-4xl text-black">Articles from the Atlantic</h1>
    <div class="flex justify-center align-center gap-4 w-full items-center">
        <!-- Button to trigger scraping news articles -->
        <button on:click={scrapeNews} class="mb-2 p-2 bg-blue-500 text-white rounded hover:bg-blue-700">
            Scrape News
        </button>
        <!-- Button to trigger fetching news articles -->
        <button on:click={fetchNews} class="mb-2 p-2 bg-green-500 text-white rounded hover:bg-green-700">
            Fetch News
        </button>

        <!-- Input field to filter headlines with form validation -->
        <form on:submit|preventDefault class="flex justify-center gap-4  ">
            <input
                type="text"
                placeholder="Search headlines..."
                bind:value={searchInput}
                class="p-2 border rounded w-full"
                required
                minlength="3"
            />
            <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 mt-2">
                Search
            </button>
        </form>
    </div>

    {#if $news.length > 0}
        {#each filterHeadlines() as article (article.id)}
            <div class="p-4 bg-white w-1/2 rounded-lg shadow-md mb-4">
                <h1 class="mb-2 text-2xl text-blue-800">Headline: {article.headline}</h1>
                <p class="mb-2">{article.summary}</p>
                <a class="text-sm text-indigo-500" href="{article.link}" target="_blank">Read more</a>
                <!-- Component to add article to favorites -->
                <AddFavorite news_id={article.id}></AddFavorite>
            </div>
        {/each}
    {/if}
</main>