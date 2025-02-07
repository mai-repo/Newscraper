<script>
    // Importing the Articles component
    import Articles from "../components/Articles.svelte";
    // Importing the userData store
    import { userData } from "../components/store.ts";
    import { goto } from "$app/navigation";
    import Pokemon from "../components/Pokemon.svelte";

    function testNavigation() {
        goto('/Favorite');
    }

</script>

<div>
    <!-- Header Section -->
    <header class="flex flex-col justify-center py-7 px-6">
        <h1 class="mb-6 text-center text-6xl font-mono text-black">
            Welcome to Mai News Scraper
        </h1>
        <nav class="flex items-center justify-between px-12">
            <!-- Displaying the user's name from the userData store -->
            <p class="px-12 text-4xl text-center">Hello, {$userData.name}</p>
            <div class="flex justify-center px-12 gap-4">
            <button on:click={testNavigation} class="mt-4 px-4 py-2 bg-blue-500 text-white rounded">
                Favorites
            </button>
            <Pokemon/>
            </div>
        </nav>
    </header>
    <!-- Including the Articles component -->
    <Articles/>
    <!-- Footer Section -->
    <footer class="py-4 mt-auto">
        <p class="text-center">&copy; 2025 Mai's Website. All rights reserved.</p>
    </footer>
</div>