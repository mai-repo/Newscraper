<script>
    import AddFavorite from "./AddFavorite.svelte";
    import Chart from "./Chart.svelte";
    import { news } from "./store.ts";
    import { Pagination } from 'flowbite-svelte';
    import { ChevronLeftOutline, ChevronRightOutline } from 'flowbite-svelte-icons';

    let searchInput = '';
    let headlineSearchInput = '';
    let summarySearchInput = '';
    let currentPage = 1;
    let totalPages = 1;
    let perPage = 10; // Number of articles per page
    let isAdvancedSearch = false; // Flag to toggle between basic and advanced search
    let isAdvancedSearchVisible = false; // Flag to show/hide advanced search form
    let showResults = false; // Flag to show/hide search results

    // Function to scrape news articles from the backend
    async function scrapeNews() {
        try {
            const response = await fetch('https://mai-newscraper.onrender.com/scrape');
            const data = await response.json();
            news.set(data); // Update the news store with scraped data
        } catch (error) {
            console.error('Error scraping news:', error);
        }
    }

    // Function to fetch news articles from the backend with pagination
    async function fetchNews(page = 1) {
        try {
            const response = await fetch(`https://mai-newscraper.onrender.com/news?page=${page}&per_page=${perPage}`);
            const data = await response.json();
            news.set(data.articles);
            currentPage = data.current_page;
            totalPages = data.total_pages;
            console.log($news);
        } catch (error) {
            console.log('Error fetching news:', error);
        }
    }

    // Function to perform a search based on the search term and search type (headline only or advanced)
    async function performSearch() {
        if (isAdvancedSearch) {
            advancedSearch();
        } else {
            basicSearch();
        }
        // Clear the search input fields after performing the search
        searchInput = '';
        headlineSearchInput = '';
        summarySearchInput = '';
        showResults = true; // Show the search results
    }

    // Basic search that filters by headline only
    function basicSearch() {
        const filteredNews = $news.filter(article =>
            article.headline.toLowerCase().includes(searchInput.toLowerCase())
        );
        news.set(filteredNews);
    }

    // Advanced search that filters by both headline and summary
    async function advancedSearch() {
        try {
            const filteredNews = $news.filter(article =>
                (article.headline.toLowerCase().includes(headlineSearchInput.toLowerCase()) ||
                article.summary.toLowerCase().includes(summarySearchInput.toLowerCase()))
            );
            news.set(filteredNews);
        } catch (error) {
            console.error('Error performing advanced search:', error);
        }
    }

    // Pagination functions
    function previousPage() {
        if (currentPage > 1) {
            fetchNews(currentPage - 1);
        }
    }

    function nextPage() {
        if (currentPage < totalPages) {
            fetchNews(currentPage + 1);
        }
    }
</script>

<main class="flex flex-col justify-center items-center py-5 gap-3">
    <h1 class="text-4xl text-black">Articles from the Atlantic</h1>
    <Chart />
    <div class="flex justify-center items-center gap-4">
        <!-- Button to trigger scraping news articles -->
        <button on:click={scrapeNews} class="p-2 bg-blue-500 text-white rounded hover:bg-blue-700">
            Scrape News
        </button>
        <!-- Button to trigger fetching news articles -->
        <button on:click={() => fetchNews(1)} class="p-2 bg-green-500 text-white rounded hover:bg-green-700">
            Fetch News
        </button>

        <!-- Input field to filter headlines with form validation -->
        <form on:submit|preventDefault class="flex justify-center gap-4">
            <input
                type="text"
                placeholder="Search headlines..."
                bind:value={searchInput}
                class="px-4 p-2 border rounded w-full"
                required
                minlength="3"
            />
            <button type="submit" on:click={performSearch} class="p-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                Search
            </button>
        </form>

        <!-- Toggle for advanced search -->
        <div>
            <label for="advanced-search" class="mr-2">Advanced Search</label>
            <input id="advanced-search" type="checkbox" bind:checked={isAdvancedSearch} on:change={() => isAdvancedSearchVisible = !isAdvancedSearchVisible} />
        </div>

        <!-- Advanced Search Form -->
        {#if isAdvancedSearchVisible}
            <div class="advanced-search-form mt-4 flex flex-col gap-3">
                <input
                    type="text"
                    placeholder="Search headlines..."
                    bind:value={headlineSearchInput}
                    class="px-4 p-2 border rounded w-full"
                    minlength="3"
                />
                <input
                    type="text"
                    placeholder="Search summaries..."
                    bind:value={summarySearchInput}
                    class="px-4 p-2 border rounded w-full"
                    minlength="3"
                />
                <button on:click={performSearch} class="p-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                    Perform Advanced Search
                </button>
            </div>
        {/if}
    </div>

    <!-- Display filtered articles only if showResults is true -->
    {#if showResults}
        {#if $news.length > 0}
            {#each $news as article (article.id)}
                <div class="p-4 bg-white w-1/2 rounded-lg shadow-md mb-4">
                    <h1 class="mb-2 text-2xl text-blue-800">Headline: {article.headline}</h1>
                    <p class="mb-2">{article.summary}</p>
                    <a class="text-sm text-indigo-500" href="{article.link}" target="_blank">Read more</a>
                    <AddFavorite news_id={article.id}></AddFavorite>
                </div>
            {/each}
        {:else}
            <p>No articles found.</p>
        {/if}
    {/if}

    <!-- Pagination Component -->
    {#if showResults}
        <Pagination {currentPage} {totalPages} on:previous={previousPage} on:next={nextPage} icon>
            <svelte:fragment slot="prev">
                <ChevronLeftOutline class="w-5 h-5" />
            </svelte:fragment>
            <svelte:fragment slot="next">
                <ChevronRightOutline class="w-5 h-5" />
            </svelte:fragment>
        </Pagination>
    {/if}
</main>
