<script>
    import AddFavorite from "./AddFavorite.svelte";
    import { news, articlesData } from "./store.ts";

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
    async function fetchNews () {
        try {
            const response = await fetch('http://127.0.0.1:5000/news');
            const data = await response.json();
            news.set(data); // Update the news store with the fetched data
        } catch (error) {
            console.log('Error fetching news:', error);
        }
    }

</script>

<main class="flex flex-col justify-center items-center py-5 gap-3">
    <h1 class="text-3xl text-red-400"> Articles from the Atlantic </h1>
    <!-- Button to trigger scraping news articles -->
    <button on:click={scrapeNews}> Scrape News </button>
    <!-- Button to trigger fetching news articles -->
    <button on:click={fetchNews}> Fetch News </button>
    {#if $news.length > 0}
        {#each $news as article (article.id)}
        <input type="text" placeholder="Search articles..." bind:value={searchInput} class="mb-4 p-2 border rounded" />
            <div class="p-4 bg-white w-1/2 rounded-lg">
                <h1 class="mb-2 text-2xl text-blue-800">Headline: {article.headline}</h1>
                <p class="mb-2">{article.summary}</p>
                <a class="text-sm text-indigo-500" href="{article.link}" target="_blank">Read more</a>
            </div>
            <!-- Component to add article to favorites -->
            <AddFavorite news_id={article.id}></AddFavorite>
        {/each}
    {/if}
</main>