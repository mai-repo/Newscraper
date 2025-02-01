<script>
    import Articles from "./Articles.svelte";
    import Form from "./Favorite.svelte";
    import { userData } from "./store.ts";
</script>

<div>

    <!-- Header Section -->
    <header class="flex flex-col justify-center py-7 px-6">
        <h1 class="mb-6 text-center text-6xl font-mono text-black">
            Welcome to Mai News Scraper
        </h1>
        <nav-bar class="flex flex-col items-center justify-center">
            <p class="p-5 text-4xl text-center">Hello, {$userData.name}</p>
            <Form />
        </nav-bar>
    </header>
    <Articles/>
    <!-- Footer Section -->
    <footer class="py-4 mt-auto">
        <p class="text-center">&copy; 2025 Mai's Website. All rights reserved.</p>
    </footer>
</div>