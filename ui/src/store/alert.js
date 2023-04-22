import { defineStore } from 'pinia'

export const useAlertStore = defineStore({
  id: 'alert',
  state: () => ({
    alert: null,
    isVisible: () => {
      return this.alert ? true : false
    },
  }),
  actions: {
    success(message) {
      this.alert = { message, type: 'alert-success' }
    },
    error(message) {
      this.alert = { message, type: 'alert-danger' }
    },
    clear() {
      this.alert = null
    },
  },
})
