<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ props }">
      <!-- <v-btn color="primary" v-bind="props"> Open Dialog </v-btn> -->
      <v-btn icon="mdi-delete" size="small" variant="flat" v-bind="props"></v-btn>
    </template>

    <v-row class="justify-center">
      <v-col cols="4">
        <v-card>
          <v-card-title class="mt-3">Delete Request</v-card-title>
          <v-card-text>Are you sure you want to <b>delete</b> this request?</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="dialog = false">Cancel</v-btn>
            <v-btn color="red" @click="deleteHandler">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-dialog>
</template>

<script setup>
import { useUsersStore } from '@/store/users'
import { useSampleStore } from '@/store/sample'
import { onMounted, ref, defineProps } from 'vue'
const usersStore = useUsersStore()
const loading = ref(true)
const dialog = ref(false)
const sampleStore = useSampleStore()
const props = defineProps({ sampleId: String })

onMounted(async () => {
  // const { users } = await usersStore.getUsers()
})

const deleteHandler = () => {
  if (!props.id) {
    console.log(`delete: `, props.sampleId)
  }
  sampleStore.deleteSampleById({ id: props.sampleId })
  dialog.value = false
}
</script>
