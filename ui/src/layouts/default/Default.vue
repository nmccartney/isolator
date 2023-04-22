<template>
  <v-app v-if="appInitialized">
    <v-layout>
      <default-bar @toggle-nav="navHandler" />
      <v-navigation-drawer v-model="drawer" location="left" temporary>
        <v-list density="compact" nav>
          <v-list-item @click="homeHandler" prepend-icon="mdi-view-dashboard" title="Dashboard"
            value="home"></v-list-item>
          <!-- <v-list-item @click="usersHandler" prepend-icon="mdi-account-group" title="Users" value="users"></v-list-item> -->
          <v-list-item @click="logoutHandler" prepend-icon="mdi-logout" title="Logout" value="logout"></v-list-item>
        </v-list>
      </v-navigation-drawer>
      <default-view />

      <Alert />
    </v-layout>
  </v-app>
</template>

<script setup>
import DefaultBar from './AppBar.vue'
import DefaultView from './View.vue'
import Alert from '@/components/Alert.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSocketStore } from '@/store/socket'
import { useApiStore } from '@/store/api'
import { useAuthStore } from '@/store/auth'

const appInitialized = ref(false)
const socketStore = useSocketStore()
const router = useRouter()
const drawer = ref(false)

onMounted(async () => {

  const api = useApiStore()
  api.create({ type: 'web' })

  appInitialized.value = true

  //begin socket integration
  // const socket = await socketStore.getSocketConnection()
  // console.log('getting socket', socket?.id)
})

const navHandler = () => {
  drawer.value = !drawer.value
}

const homeHandler = () => {
  router.push({
    name: 'Home',
  })
}

const logoutHandler = () => {
  const authStore = useAuthStore()
  authStore.logout()
  router.push({
    name: 'login',
  })
}
</script>
