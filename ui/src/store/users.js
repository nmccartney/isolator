import { defineStore } from 'pinia'
import { useApiStore } from '@/store/api'
import { useAlertStore } from '@/store/alert'

export const useUsersStore = defineStore({
  id: 'users',
  state: () => ({
    // initialize state from local storage to enable user to stay logged in
    user: JSON.parse(localStorage.getItem('user')),
    users: [],
  }),
  getters: {
    userById() {
      return {}
    },
  },
  actions: {
    async getUsers() {
      try {
        const api = useApiStore()
        const { data } = await api.get(`/users`)
        this.users = data.results
        return { users: data.results }
      } catch (error) {
        console.warn(error)
        const { response } = error
        const errorMessage = response.data.message
        const alertStore = useAlertStore()
        alertStore.error(errorMessage)
        return { error: errorMessage }
      }
    },
  },
})
