<template>
  <div>
    <v-row class="pt-4 ml-4">
      <v-col cols="4" id="request-detail-side-panel">
        <v-card>
          <v-card-title class="">
            <v-btn @click="handleBackBtn" icon="mdi-chevron-left" class="text-secondary" size="lrg"
              variant="flat"></v-btn>

            Sample {{ sampleModel.name }}

            <v-chip size="small" :color="getColor(sampleModel)">
              <span>{{ sampleModel.status }}</span>
            </v-chip>
          </v-card-title>
          <v-divider></v-divider>
          <div class="pa-4">
            test
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { useSampleStore } from '@/store/sample'
import { onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
const loading = ref(true)
const sampleModel = ref(true)
const participantsList = ref([])
const router = useRouter()
const sampleStore = useSampleStore()


onMounted(async () => {
  const route = useRoute()
  const { sample, error } = await sampleStore.getSampleById({ id: route.params.sampleId })
  if (error) {
    console.warn(error)
    return
  }
  sampleModel.value = sample

  console.log(`viewing sample: `, sample)
})

const handleBackBtn = () => {
  router.push({ name: 'Samples' })
}

const handleSampleChange = (sample) => {
  sampleModel.value = sample
}


const getColor = (item) => {
  if (!item.approved && item.denied) return 'red'
  else if (item.approved && !item.denied) return 'green'
  else return 'orange'
}
</script>
<style>
.table-wrapper {
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 10px;
}
</style>
