<script>
    import { onMount } from 'svelte';
    import { API_BASE_URL } from '../../config.js';
    let pokemon = null;
    let image = '';


    // Function to fetch favorite Pokemon data
    async function pokemonData(){
        try {
            const response = await fetch(`${API_BASE_URL}/getPokemon`);
            const data = await response.json();

            if (data){
                console.log("Success grabbing Favorite Pokemon Data!");
                pokemon = data; // Update the pokemon variable with fetched data
            }
        } catch (error) {
            console.error("Error fetching Pokemon");
        }

    }

    // Function to delete a Pokemon by id
    async function deletePokemon(id) {
        try {
            const response = await fetch(`${API_BASE_URL}/deletePokemon/${id}`, {
                method: "DELETE",
            });
            if (response.ok) {
                console.log("Pokemon deleted successfully!");
                pokemon = pokemon.filter(p => p.id !== id); // Remove the deleted Pokemon from the list
            } else {
                const errorData = await response.json();
                console.log(errorData.message);
            }
        } catch (error) {
            console.log("Error deleting Pokemon:", error);
        }
    }

    // Function to update the Pokemon's profile image
    async function updatePhoto(id, image) {
        const data = {
            pokemon_id: id,
            image: image
        };
        try {
            const response = await fetch(`${API_BASE_URL}/changeProfile`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
            console.log("Photo updated successfully!");
        } else {
            // Ensure the response body is available before accessing it
            let errorData = await response.json().catch(() => ({ message: "Unknown error" }));
            console.error("Error updating photo:", errorData.message || "Unknown error");
            console.log("Sent data:", data);
        }
    } catch (error) {
        console.error("Error updating photo:", error);
    }
    }
    onMount(() => {
        pokemonData();
    });
</script>

{#if pokemon}
    <div class="justify-center mb-8 bg-white p-3 rounded border outline-black">
        {#each pokemon as p (p.id)}
            <!-- Display Pokemon name -->
            <h2 style="color: blue; font-size: 24px; margin-bottom: 10px;">{p.pokemonName.toUpperCase()}</h2>
            <div>
                <!-- Display Pokemon image -->
                <img src={p.image} alt={p.Name} />
                <!-- Form to update Pokemon image -->
                <div class="flex gap-3">
                    <form on:submit|preventDefault={() => updatePhoto(p.id, image)}>
                        <input type="text" bind:value={image} placeholder="Enter new image URL" style="border: 1px solid black; padding: 8px; border-radius: 4px" />
                        <button class="x-4 p-2 mb-4 bg-green-700 text-white rounded hover:bg-blue-700 submit">Change Profile Image</button>
                    </form>
                    <button class="x-4 p-2 mb-4 bg-pink-700 text-white rounded hover:bg-blue-700" on:click={() => deletePokemon(p.id)}>Delete Pokemon</button>
                </div>

            </div>
            <!-- Button to delete Pokemon -->

        {/each}
    </div>
{/if}
