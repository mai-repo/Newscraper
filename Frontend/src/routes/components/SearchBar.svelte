<script>
    import { articlesData } from "./store.ts";
    let searchInput = '';
     // Function to filter articles based on the search query
    function filterArticles() {
        return $articlesData.filter(article =>
            article.headline.toLowerCase().includes(searchInput.toLowerCase())
        );
    }
</script>

<input type="text" placeholder="Search articles..." bind:value={searchInput} class="mb-4 p-2 border rounded" />