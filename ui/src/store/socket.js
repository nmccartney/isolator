// Utilities
import { defineStore } from 'pinia'
import { ref, onMounted, getCurrentInstance } from 'vue'
import { io } from 'socket.io-client'
import { useUsersStore } from './users'
import { useAlertStore } from '@/store/alert'

export const useSocketStore = defineStore('socket', {
  state: () => ({
    socket: {},
    connection: false,
    usersOnline: [],
    vehiclesOnline: [],
  }),
  getters: {
    getSocket(state) {
      return this.socket
    },
    isConnected() {
      return this.connection
    },
  },
  actions: {
    disconnect() {
      //first we need to remove user from online users list
      let onlineUserIds = this.usersOnline.map((u) => u.id)
      let userIndex = onlineUserIds.indexOf(this.socket.auth.user)
      this.usersOnline.splice(userIndex, 1)
      // now we can execute disconnection cmd
      this.socket.disconnect()
    },
    async getSocketConnection() {
      const $state = this
      return new Promise((resolve, reject) => {
        try {
          const userStore = useUsersStore()
          // TODO: setup ENV VAR for below address
          const domainsSplit = String(document.location).split(':')
          const domain = `${domainsSplit[0]}:${domainsSplit[1]}`
          const socket = io(`${domain}:3030`, {
            auth: {
              user: userStore.$state.user.id,
            },
          })

          this.socket = socket

          socket.on('connect', (s) => {
            console.log(`socket: got connection `, socket.id)
            this.connection = true
            resolve(socket)
          })

          socket.on('disconnect', () => {
            console.log(`socket: disconnected`, socket.id) // undefined
            this.connection = false
          })

          // User Listeners
          socket.on('user/online', (s) => {
            console.log(`socket: user/online `, s)
            // TODO: find a better way to get the user from below
            let user = s.users.reduce((acc, val) => {
              if (!acc) acc = {}
              if (acc.id === s.user) return acc
              if (val.id === s.user) return val
              return { ...acc }
            })
            console.log('users online ', s.users)
            $state.usersOnline = s.users
            const alertStore = useAlertStore()
            alertStore.success(`User now online ${user.email}`)
          })

          socket.on('user/offline', (s) => {
            console.log(`socket: user/offline `, s)
            $state.usersOnline = s.users
            const alertStore = useAlertStore()
            alertStore.success(`User now offline ${s.user?.email}`)
          })

          // Vehicle listeners
          socket.on('vehicle/online', (s) => {
            console.log(`socket: vehicle/online `, s)
            // TODO: find a better way to get the vehicle from below
            let vehicle = s.vehicles.reduce((acc, val) => {
              if (!acc) acc = {}
              if (acc.id === s.user) return acc
              if (val.id === s.user) return val
              return { ...acc }
            })

            $state.vehiclesOnline = s.vehicles
            const alertStore = useAlertStore()
            alertStore.success(`Vehicle now online ${vehicle.name}`)
          })

          socket.on('vehicle/offline', (s) => {
            console.log(`socket: vehicle/offline `, s)
            $state.vehiclesOnline = s.vehicles
            const alertStore = useAlertStore()
            alertStore.success(`Vehicle now offline ${s.vehicle.name}`)
          })
        } catch (err) {
          console.warn(`socket-conneciton: `, err)
          reject()
        }
      })
    },
    async getUsers() {
      return new Promise((resolve, reject) => {
        const filter = {}
        const options = { sortBy: false, limit: 10, page: 1 }
        try {
          const resp = this.socket.emit('users/query', { filter, options }, (res) => {
            resolve(res)
          })
        } catch (err) {
          console.warn(err)
          reject()
        }
      })
    },
    async getPresentUsers() {
      const $state = this
      return new Promise((resolve, reject) => {
        try {
          const resp = this.socket.emit('users/present', {}, (res) => {
            $state.usersOnline = res.users
            resolve(res)
          })
        } catch (err) {
          console.warn(err)
          reject()
        }
      })
    },
    async getOnlineVehicles() {
      const $state = this
      return new Promise((resolve, reject) => {
        try {
          const resp = this.socket.emit('vehicle/online', {}, (res) => {
            $state.vehiclesOnline = res.vehicles
            resolve(res)
          })
        } catch (err) {
          console.warn(err)
          reject()
        }
      })
    },
  },
})
