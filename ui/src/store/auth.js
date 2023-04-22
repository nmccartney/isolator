import { defineStore } from 'pinia'
import axios from 'axios'
import { useAlertStore } from '@/store/alert'
import { useApiStore } from '@/store/api'

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    // initialize state from local storage to enable user to stay logged in
    user: JSON.parse(localStorage.getItem('user') !== 'undefined' ? localStorage.getItem('user') : null),
    returnUrl: null,
  }),
  getters: {
    isAuthenticated() {
      return !this.user ? false : true
    },
  },
  actions: {
    async login(username, password) {
      try {
        const api = useApiStore()
        const { data } = await api.post(`/auth/login`, { email: username, password })
        // update pinia state
        this.user = data.user
        const token = data.tokens
        // store user details and jwt in local storage to keep user logged in between page refreshes
        localStorage.setItem('user', JSON.stringify(this.user))
        localStorage.setItem('token', JSON.stringify(token))

        return { user: this.user }
      } catch (error) {
        console.warn(error)
        const { response } = error
        // handler network error message
        if (!error.response) {
          const errorMessage = `${error.message} - Check your Server`
          const alertStore = useAlertStore()
          alertStore.error(errorMessage)
          return { error: errorMessage }
        }
        const errorMessage = response.data.message
        const alertStore = useAlertStore()
        alertStore.error(errorMessage)
        return { error: errorMessage }
      }
    },
    logout() {
      this.user = null
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    },
  },
})
