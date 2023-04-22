<template>
  <!-- <div v-if="alert" class="container">
      <div class="m-3">
        <div class="alert alert-dismissable" :class="alert.type">
          <button @click="alertStore.clear()" class="btn btn-link close">×</button>
          {{ alert.message }}
        </div>
      </div>
    </div> -->
  <v-snackbar v-model="snackbar">
    {{ alert.message }}

    <template v-slot:actions>
      <v-btn :color="colorRef" variant="text" @click="close()"> Close </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useAlertStore } from '@/store/alert'
const snackbar = ref(false)
const colorRef = ref('red')
const alertStore = useAlertStore()
const { alert, isVisible } = storeToRefs(alertStore)
// let alert = {}

const unsubscribe = alertStore.$onAction(({ name, success }) => {
  if (name == 'error') {
    colorRef.value = 'red'
    snackbar.value = true
  }
  if (name == 'success') {
    colorRef.value = 'green'
    snackbar.value = true
  }
})

const close = () => {
  // console.log(`alert: `, alert.value)
  snackbar.value = false
  // alertStore.clear()
}
</script>
