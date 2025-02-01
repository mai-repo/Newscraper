import { writable } from "svelte/store";


export const userData = writable({});
export const message = writable(false);
export const articlesData = writable([]);
export const favArticles = writable([]);
export const news = writable([]);

/*
Further information on stores in svelte from the official documentation:
A store is an object that allows reactive access to a value via a simple store contract. The svelte/store module contains minimal store implementations which fulfil this contract.

Any time you have a reference to a store, you can access its value inside a component by prefixing it with the $ character. This causes Svelte to declare the prefixed variable,
subscribe to the store at component initialisation and unsubscribe when appropriate.
*/
