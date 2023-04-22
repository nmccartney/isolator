<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ props }">
      <!-- <v-btn color="primary" v-bind="props"> Open Dialog </v-btn> -->

      <div class="mt-5 mr-8">
        <v-btn prepend-icon="mdi-plus" size="small" color="secondary" variant="tonal" v-bind="props">New Sample</v-btn>
      </div>
    </template>

    <v-row class="justify-center">
      <v-col cols="4">
        <v-card>
          <form @submit="submit">
            <v-card-title class="mt-3 mb-2">New Sample</v-card-title>
            <v-card-text>
              <v-text-field v-model="name.value.value" :error-messages="name.errorMessage.value" required label="Name"
                type="text"></v-text-field>
              <v-file-input v-model="file.value.value" :error-messages="file.errorMessage.value"
                label="File input"></v-file-input>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <!-- <v-btn @click="dialog = false">Cancel</v-btn>
              <v-btn color="primary" @click="dialog = false">Create</v-btn> -->
              <v-btn @click="dialog = false">Cancel</v-btn>
              <v-btn color="primary" :disabled="isSubmitting" type="submit">Create</v-btn>
            </v-card-actions>
          </form>
        </v-card>
      </v-col>
    </v-row>
  </v-dialog>
</template>

<script setup>
import { useUsersStore } from '@/store/users'
import { useSampleStore } from '@/store/sample'
import { onMounted, ref } from 'vue'
import { useField, useForm } from 'vee-validate'
import * as Yup from 'yup'

const loading = ref(true)
const dialog = ref(false)
const usersStore = useUsersStore()
const sampleStore = useSampleStore()
const usersRef = ref([])

const schema = Yup.object().shape({
  name: Yup.string().required('Name is required'),
  file: Yup.mixed().required('File is required'),
})

const { handleSubmit, handleReset, isSubmitting } = useForm({
  //   initialValues: formValues,
  validationSchema: schema,
})

const name = useField('name')
const file = useField('file')

onMounted(async () => {
  // const { users } = await usersStore.getUsers()
  // usersRef.value = users
})

function onInvalidSubmit({ values, errors, results }) {
  console.log('invalid!!')
  console.log(values) // current form values
  console.log(errors) // a map of field names and their first error message
  console.log(results) // a detailed map of field names and their validation results
}

const submit = handleSubmit(async (values) => {
  console.log(`testing`, values)
  const { name, file } = values
  var formData = new FormData();
  formData.append("file", file);
  const { sample, error } = await sampleStore.getNewSample({
    formData
  })
  //   form.value.reset()
  if (error) {
    console.warn(error)
  }
  if (sample) {
    console.log('created sample')
    handleReset()
    dialog.value = false
  }
}, onInvalidSubmit)
</script>
