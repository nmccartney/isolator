/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import { loadFonts } from './webfontloader'
import vuetify from './vuetify'
import pinia from '../store'
import router from '../router'

// import { createPinia } from 'pinia'
// const pinia = createPinia()

export function registerPlugins(app) {
  loadFonts()
  app.use(pinia).use(vuetify).use(router)
}
