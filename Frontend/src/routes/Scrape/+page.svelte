<script>
    // Importing the Articles component
    import Articles from "../components/Articles.svelte";
    // Importing the userData store
    import { userData } from "../components/store.ts";
    import { goto } from "$app/navigation";
    import Pokemon from "../components/Pokemon.svelte";
    import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';


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
        <Navbar class="flex items-center justify-between px-12 bg-pink-200">
            <NavBrand>
            <p class="px-12 text-4xl text-center text-black">Hello, {$userData.name}</p>
            </NavBrand>

            <NavHamburger />
            <NavUl class="flex justify-center">
                <NavLi class="text-xl text-black rounded" href='/Favorite'>Favorites</NavLi>
            </NavUl>
            <Pokemon/>
        </Navbar>

    </header>
    <!-- Including the Articles component -->
    <Articles/>
    <!-- Footer Section -->
    <footer class="py-4 mt-auto">
        <p class="text-center">&copy; 2025 Mai's Website. All rights reserved.</p>
    </footer>
</div>