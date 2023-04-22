<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex fill-height">
      <v-sheet class="pt-2">
        <!-- HEADER SECTION -->
        <v-row class="mb-2">
          <v-col class="pt-6 pl-8">
            <span class="text-subtitle">Sample Management </span>
          </v-col>
          <v-spacer></v-spacer>
          <SampleNewDialog />
        </v-row>

        <v-divider class="mt-2"></v-divider>

        <!-- TABLE SECTION -->
        <v-data-table-server :headers="headers" :items="samples" :items-length="1" :loading="loading" :items-per-page="2"
          item-value="name" show-select show-expand class="elevation-1">
          <template v-slot:item.status="{ item }">
            <v-chip size="small" :color="getColor(item.raw)">
              {{ item.status }}
            </v-chip>
          </template>
          <template v-slot:item.actions="{ item }">
            <SampleEditDialog :order-id="item.raw.id" />
            <v-btn @click="handleViewRequest(item.raw.id)" icon="mdi-eye" size="small" variant="flat"></v-btn>
            <SampleDeleteDialog :order-id="item.raw.id" />
          </template>
          <template v-slot:expanded-row="{ item }">
            <tr>
              <td colspan="12">{{ item }}</td>
            </tr>
          </template>
        </v-data-table-server>
      </v-sheet>
    </v-responsive>
  </v-container>
</template>

<script setup>
import SampleNewDialog from '@/components/samples/SampleNewDialog.vue'
import SampleEditDialog from '@/components/samples/SampleEditDialog.vue'
import SampleDeleteDialog from '@/components/samples/SampleDeleteDialog.vue'
import { useSampleStore } from '@/store/sample'
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const sampleStore = useSampleStore()
const loading = ref(true)
const headers = [
  {
    title: 'Name',
    align: 'start',
    sortable: true,
    key: 'name',
  },
  { title: 'Status', key: 'status', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false },
]

const samples = computed(() => {
  // let ordsamplesers = sampleStore.$state.samples.map((order) =>
  //   Object.assign({ ...order })
  // )
  return sampleStore.$state.samples
})

onMounted(async () => {
  await sampleStore.getSamples()
  setTimeout(() => {
    loading.value = false
  }, 400)
})

const handleViewRequest = (id) => {
  router.push({ name: 'SampleDetail', params: { requestId: id } })
}

const getColor = (item) => {
  if (item.status === 'FAILED') return 'red'
  else if (item.status === 'SUCCESS') return 'green'
  else return 'orange'
}
</script>
