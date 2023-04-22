/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'


// const app = createApp(App)

// registerPlugins(app)

// app.mount('#app')

window.addEventListener('DOMContentLoaded', async () => {
    const app = createApp(App)
    try {
        registerPlugins(app)
        app.mount('#app');
    } catch (err) {
        console.log(`Error: ${err}`);
        throw new Error(`Error: ${err}`)
    }
});