<template>
  <v-app-bar flat>
    <!-- <v-icon @click="menuClickHandler" icon="mdi-menu" /> -->
    <v-btn color="white" @click="menuClickHandler" icon="mdi-menu"></v-btn>
    <!-- <v-btn color="white" @click="menuClickHandler" icon="mdi-close"></v-btn> -->
    <v-app-bar-title>
      <span class="" @click="appClickHandler">Isolator</span>
    </v-app-bar-title>
    <v-spacer></v-spacer>
    <div class="mr-4">
      <v-menu>
        <template v-slot:activator="{ props }">
          <!--  -->
          <v-btn variant="flat" v-bind="props">
            <v-badge v-model="isConnected" dot color="success">
              <v-icon>mdi-radio-tower</v-icon>
            </v-badge>
          </v-btn>
        </template>

        <v-list density="compact">
          <v-list-subheader>Connections</v-list-subheader>
          <v-list-item>
            <template v-slot:prepend>
              <v-badge v-model="isServerConnection" dot color="success">
                <v-icon icon="mdi-server"></v-icon>
              </v-badge>
            </template>
            <v-list-item-title class="ml-4">Server </v-list-item-title>
            <template v-slot:append>
              <v-switch class="ml-8" @click.stop="onServerConnectionClick($event)" color="green" inset
                v-model="serverConnectionModel" density="compact" hide-details></v-switch>
            </template>
          </v-list-item>
        </v-list>
      </v-menu>
      <!--  -->
      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn variant="flat" icon="mdi-cog" size="small" v-bind="props"></v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title>
              <v-switch color="white" inset @click.stop="() => { }" label="Theme" density="compact"></v-switch>
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>
  </v-app-bar>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { onMounted, ref, computed } from 'vue'
import { useSocketStore } from '@/store/socket'

const socketStore = useSocketStore()
const router = useRouter()
const emit = defineEmits(['toggleNav'])
const serverConnectionModel = ref(false)

const isServerConnection = computed(() => {
  console.log('getting server conneciton status', socketStore.$state.connection)
  serverConnectionModel.value = socketStore.$state.connection
  return socketStore.$state.connection
})

const isConnected = computed(() => {
  return isServerConnection.value
})

const menuClickHandler = () => {
  // pass nav state up to parent
  emit('toggleNav')
}

const onServerConnectionClick = async (e) => {
  if (isServerConnection.value) {
    socketStore.disconnect()
  } else {
    await socketStore.getSocketConnection()
  }
}

const appClickHandler = () => {
  router.push({
    name: 'Home',
  })
}
</script>
<style>
.no-click-zone {
  pointer-events: none;
}
</style>
