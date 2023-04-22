<template>
  <v-app>
    <default-view v-if="appInitialized" />
    <Alert />
  </v-app>
</template>

<script setup>
import DefaultView from './View.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Alert from '@/components/Alert.vue'
import { useApiStore } from '@/store/api'

const router = useRouter()
const drawer = ref(false)
const appInitialized = ref(false)

onMounted(async () => {

  const api = useApiStore()
  api.create({ type: 'web' })

  appInitialized.value = true
})
</script>
