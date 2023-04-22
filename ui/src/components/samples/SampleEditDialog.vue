<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ props }">
      <!-- <v-btn color="primary" v-bind="props"> Open Dialog </v-btn> -->
      <v-btn icon="mdi-pencil" size="small" variant="flat" v-bind="props"></v-btn>
    </template>

    <v-row class="justify-center" v-if="dialog">
      <v-col cols="4">
        <v-card>
          <v-card-title class="mt-3">Edit Request</v-card-title>
          <form @submit="submit">
            <v-card-text>
              <v-text-field v-model="name.value.value" :error-messages="name.errorMessage.value" label="Name"
                type="text"></v-text-field>
              <v-text-field readonly v-model="owner.value.value" :error-messages="owner.errorMessage.value" id="owner"
                label="Owner"></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click="dialog = false">Cancel</v-btn>
              <v-btn color="primary" :disabled="isSubmitting" type="submit">Update</v-btn>
            </v-card-actions>
          </form>
        </v-card>
      </v-col>
    </v-row>
  </v-dialog>
</template>

<script setup>
import { useSampleStore } from '@/store/sample'
import { onMounted, ref } from 'vue'
import { useField, useForm } from 'vee-validate'
import * as Yup from 'yup'
const loading = ref(true)
const dialog = ref(false)
const sampleStore = useSampleStore()
const props = defineProps({ orderId: String })

const schema = Yup.object().shape({
  name: Yup.string().required('Name is required'),
})

const { handleSubmit, setValues, isSubmitting } = useForm({
  //   initialValues: formValues,
  validationSchema: schema,
})

const name = useField('name')

onMounted(async () => {
  if (!props?.sampleId) return

  const { sample, error } = await sampleStore.getSampleById({ id: props.sampleId })
  if (error) {
    console.warn(error)
    return
  }
  if (sample) {
    setValues({
      name: sample.name,
    })
  }
})

function onInvalidSubmit({ values, errors, results }) {
  console.log('invalid!!')
  console.log(values) // current form values
  console.log(errors) // a map of field names and their first error message
  console.log(results) // a detailed map of field names and their validation results
}
const submit = handleSubmit(async (values) => {
  const { name } = values
  const { sample, error } = await sampleStore.updateSampleById({ id: props.sampleId, sample: { name } })
  if (error) {
    console.warn(error)
    return
  }
  if (sample) {
    dialog.value = false
  }
}, onInvalidSubmit)
</script>
