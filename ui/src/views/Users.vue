<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex fill-height">
      <v-sheet class="pt-2">
        <v-row class="mb-2">
          <v-col class="pt-6 pl-8">
            <span class="text-subtitle">User Management </span>
          </v-col>
          <v-spacer></v-spacer>
          <!-- <v-col class="pt-6"><RequestNewDialog /></v-col> -->
          <!-- <RequestNewDialog /> -->
        </v-row>

        <v-divider class="mt-2"></v-divider>
        <v-data-table-server :headers="headers" :items="usersRef" :items-length="1" :loading="loading" :items-per-page="2"
          item-value="name" show-select class="elevation-1">
        </v-data-table-server>
      </v-sheet>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { useUsersStore } from '@/store/users'
import { onMounted, ref } from 'vue'
const usersStore = useUsersStore()
const loading = ref(true)
const headers = [
  {
    title: 'Name',
    align: 'start',
    sortable: true,
    key: 'name',
  },
  { title: 'Role', key: 'role' },
  { title: 'Email', key: 'email' },
  { title: 'Created', key: 'createdAt' },
  { title: 'Updated', key: 'updatedAt' },
]

const usersRef = ref([])

onMounted(async () => {
  const { users } = await usersStore.getUsers()
  setTimeout(() => {
    loading.value = false
  }, 500)
  if (users) {
    usersRef.value = users
  }
})
</script>
