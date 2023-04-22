// Utilities
import { defineStore } from 'pinia'
import axios from 'axios'

const API_VERSION = 'v1'
const DEFAULT_API_TIMEOUT = 1000
const domainsSplit = String(document.location).split(':')
const domain = `${domainsSplit[0]}:${domainsSplit[1]}`
const DEFAULT_API_URL = `${domain}:5000/${API_VERSION}`
/**
 * This store is to hold an instance of the api
 * This store also determins which http library to use
 * For web/browser use, were using axios
 * For mobile were using capacitor's http libarry for native access
 * ref: https://capacitorjs.com/docs/apis/http#api
 */
export const useApiStore = defineStore('api', {
  state: () => ({
    //
    API: null,
    baseUrl: JSON.parse(
      localStorage.getItem('server') !== 'undefined' ? localStorage.getItem('server') : DEFAULT_API_URL
    ),
    type: 'web', // web || native
  }),
  getters: {
    serverUrl() {
      if (localStorage.getItem('server') !== 'undefined' && localStorage.getItem('server') !== null) {
        return JSON.parse(localStorage.getItem('server')).url
      }
      return DEFAULT_API_URL
    },
    apiStatus() {
      return this.API ? true : false
    },
  },
  actions: {
    create({ url, type }) {
      if (!url) {
        // check to see if there is one saved
        if (localStorage.getItem('server') !== 'undefined' && localStorage.getItem('server') !== null) {
          let serverUrl = JSON.parse(localStorage.getItem('server')).url
          this.baseUrl = serverUrl
        } else {
          this.baseUrl = DEFAULT_API_URL
        }
      } else {
        this.baseUrl = `${url}/v1`
        localStorage.setItem('server', JSON.stringify({ url: this.baseUrl }))
      }

      this.API = axios.create({
        baseURL: `${this.baseUrl}`,
        timeout: DEFAULT_API_TIMEOUT,
      })

      if (!type) this.type = 'web' // default to web
      this.type = type

      return this.API

      // TODO: determine which is the best http library to use axios or capacitor's http
      // if (this.type === 'web') {
      //   this.API = axios.create({
      //     baseURL: `${this.baseURL}`,
      //     timeout: DEFAULT_API_TIMEOUT,
      //   })
      // } else {
      //   this.API = CapacitorHttp
      // }
    },
    async get(url, options) {
      if (!this.API) throw Error({ message: 'No API created' })
      return await this.API.get(url)

      // TODO: determine which is the best http library to use axios or capacitor's http
      // if (this.type === 'web') {
      //   return await this.API.get(url, options)
      // } else {
      //   return await this.API.get({ url: `${this.baseURL}${url}`, ...options })
      // }
    },
    async post(url, data, options) {
      if (!this.API) throw Error({ message: 'No API created' })
      return await this.API.post(url, data, options)

      // TODO: determine which is the best http library to use axios or capacitor's http
      // if (this.type === 'web') {
      //   return await this.API.post(url, options)
      // } else {
      //   return await this.API.post({ url: `${this.baseURL}${url}`, data: options })
      // }
    },
    async patch(url, options) {
      if (!this.API) throw Error({ message: 'No API created' })
      return await this.API.patch(url, options)

      // TODO: determine which is the best http library to use axios or capacitor's http
      // if (this.type === 'web') {
      //   return await this.API.patch(url, options)
      // } else {
      //   return await this.API.patch({ url: `${this.baseURL}${url}`, data: options })
      // }
    },
    async delete(url, options) {
      if (!this.API) throw Error({ message: 'No API created' })
      return await this.API.delete(url, options)

      // TODO: determine which is the best http library to use axios or capacitor's http
      // if (this.type === 'web') {
      //   return await this.API.delete(url, options)
      // } else {
      //   return await this.API.delete({ url: `${this.baseURL}${url}`, data: options })
      // }
    },
  },
})
