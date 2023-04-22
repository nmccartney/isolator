<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex fill-height">
      <v-row>
        <v-col><v-btn>Isolate Sample</v-btn></v-col>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useUsersStore } from '@/store/users'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()

const userStore = useUsersStore()
const currUser = computed(() => {
  return userStore.$state.user
})


onMounted(async () => { })
</script>
