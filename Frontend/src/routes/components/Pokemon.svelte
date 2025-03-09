<script>
    import { API_BASE_URL } from '../../config.js';
    import { userData, pokemonData} from './store.ts';
    import { get } from 'svelte/store';

    let pokemonName = '';
    let pokemon = null;
    let username = '';

    // Subscribe to the userData store to get the username
    $: username = get(userData).name;

    // Fetch function to get Pokémon data based on the name
    async function fetchPokemon(name) {
        try {
            // Make the GET request with the Pokémon name
            const response = await fetch(`${API_BASE_URL}/catchEm?name=${name}`);
            const data = await response.json();

            // If data is received successfully, set it to the pokemon variable
            if (data) {
                pokemon = data;
            }
        } catch (error) {
            console.log("Error fetching Pokémon");
        }
    }

    // Save function to save Pokémon data
    async function addPokemon() {
        // Ensure pokemon and pokemon.image are valid before sending the request
        if (!pokemon || !pokemon.image) {
            console.log("Error: Pokémon data is incomplete.");
            return;
        }

        try {
            // Make the POST request to save the Pokémon data
            const response = await fetch(`${API_BASE_URL}/savePokemon`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    pokemonName: pokemonName,
                    image: pokemon.image,
                }),
            });

            // Check if the response is not OK (status code is not in the range 200-299)
            if (!response.ok) {
                const errorData = await response.json();
                console.log("Error saving Pokémon:", errorData);
                return;
            }

            const data = await response.json();

            if (data.message) {
                pokemonData.set(data);
                console.log(data.message);
                alert("successfully added Pokemon")

            } else {
                console.log("Unexpected response structure:", data);
            }
        // Log any errors that occur during the save process
    } catch (error) {
            console.log("Error saving and catching the Pokémon:", error);
        }
    }
</script>

<main>
    <div class="flex justify-center gap-2">
            <!-- Form to input Pokémon name and fetch data -->
    <form class="justify-space-evenly items-center" on:submit|preventDefault={() => fetchPokemon(pokemonName)}>
        <!-- Input field for Pokémon name -->
        <input
            bind:value={pokemonName}
            placeholder="Enter Pokémon name"
            class="mt-4 px-4 py-2 text-black rounded mr-4"
            required
        />
        <!-- Button to submit the form and fetch Pokémon data -->
        <button class="mt-4 p-2 bg-blue-500 text-white rounded" type="submit">Catch Pokémon!</button>
    </form>

    <!-- Display the fetched Pokémon data -->
    {#if pokemon}
            <button class=" mt-4 p-2 p-2 bg-green-500 text-white rounded" on:click={addPokemon}>Add to Favorites</button>
    {/if}
    </div>
</main>
