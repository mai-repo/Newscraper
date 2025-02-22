import { writable } from "svelte/store";


let storedUserData = null;
if (typeof window !== "undefined") {
    storedUserData = sessionStorage.getItem("userData");
}

export const userData = writable(storedUserData ? JSON.parse(storedUserData) : { name: '' });

if (typeof window !== "undefined") {
    userData.subscribe(value => {
        if (value) {
            sessionStorage.setItem("userData", JSON.stringify(value));
        }
    });
}

export const message = writable(false);
export const articlesData = writable([]);
export const favArticles = writable([]);
export const news = writable([]);
export const pokemonData = writable([]);
export const profilePhoto = writable([]);

/*
Further information on stores in svelte from the official documentation:
A store is an object that allows reactive access to a value via a simple store contract. The svelte/store module contains minimal store implementations which fulfil this contract.

Any time you have a reference to a store, you can access its value inside a component by prefixing it with the $ character. This causes Svelte to declare the prefixed variable,
subscribe to the store at component initialisation and unsubscribe when appropriate.
*/
