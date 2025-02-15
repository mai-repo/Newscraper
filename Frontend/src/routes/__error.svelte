<script context="module">
    export function load({ error, status }) {
      return {
        props: { error, status }
      };
    }
  </script>

  <script>
    export let error;
    export let status;
  </script>

  <svelte:head>
    <title>{status} - {error.message}</title>
  </svelte:head>

  <main class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="text-center p-6 bg-white shadow-md rounded-md">
      <h1 class="text-6xl font-bold text-red-500">{status}</h1>
      <h2 class="text-2xl mt-4">{error.message}</h2>
      <a href="/" class="mt-6 inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700">Return Home</a>
    </div>
  </main>

  <style>
    main {
      font-family: Arial, sans-serif;
    }
  </style>