<script>
    // Importing the Articles component
    import Articles from "./Articles.svelte";
    // Importing the Form component
    import Favorite from "./Favorite.svelte";
    // Importing the userData store
    import { userData } from "./store.ts";
</script>

<div>
    <!-- Header Section -->
    <header class="flex flex-col justify-center py-7 px-6">
        <h1 class="mb-6 text-center text-6xl font-mono text-black">
            Welcome to Mai News Scraper
        </h1>
        <nav-bar class="flex flex-col items-center justify-center">
            <!-- Displaying the user's name from the userData store -->
            <p class="p-5 text-4xl text-center">Hello, {$userData.name}</p>
            <!-- Including the Form component -->
            <Favorite />
        </nav-bar>
    </header>
    <!-- Including the Articles component -->
    <Articles/>
    <!-- Footer Section -->
    <footer class="py-4 mt-auto">
        <p class="text-center">&copy; 2025 Mai's Website. All rights reserved.</p>
    </footer>
</div>