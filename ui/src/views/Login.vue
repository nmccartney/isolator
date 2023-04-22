<template>
  <v-sheet class="d-flex align-center justify-center" height="100vh">
    <v-card class="login-card elevation-12">
      <form @submit="submit">
        <v-toolbar dark color="secondary">
          <v-toolbar-title>Isolator</v-toolbar-title>
        </v-toolbar>
        <v-card-text class="mt-2">
          <v-text-field v-model="username.value.value" :error-messages="username.errorMessage.value" label="Username"
            type="text"></v-text-field>
          <v-text-field v-model="password.value.value" :error-messages="password.errorMessage.value" id="password"
            label="Password" type="password"></v-text-field>
          <!-- Mobile Only Area -->
          <div>
            <v-expansion-panels>
              <v-expansion-panel title="Advanced">
                <v-expansion-panel-text>
                  <v-text-field v-model="server.value.value" :error-messages="server.errorMessage.value"
                    label="Server address" type="text"></v-text-field>
                  <!-- {{ deviceInfo }} -->
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <!-- <v-btn color="primary" to="/">Login</v-btn> -->
          <!-- <v-btn @click="handleReset">clear</v-btn> -->

          <v-btn color="primary" :disabled="isSubmitting" type="submit">Login</v-btn>
        </v-card-actions>
      </form>
    </v-card>
  </v-sheet>
</template>
<style>
.login-card {
  min-width: 400px;
  max-width: 600px;
}
</style>
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
// import { Form, Field } from 'vee-validate'
import { useField, useForm } from 'vee-validate'
import * as Yup from 'yup'

import { useAuthStore } from '@/store/auth'
import { useApiStore } from '@/store/api'
const router = useRouter()
const drawer = ref(false)

const schema = Yup.object().shape({
  username: Yup.string().required('Username is required'),
  password: Yup.string().required('Password is required'),
})

const formValues = {
  username: 'example@example.com',
  password: 'P@$$w0Rd',
}
const { handleSubmit, handleReset, isSubmitting, setFieldValue } = useForm({
  //   initialValues: formValues,
  validationSchema: schema,
})

const username = useField('username')
const password = useField('password')
const server = useField('server')

onMounted(async () => {
  const domainsSplit = String(document.location).split(':')
  const domain = `${domainsSplit[0]}:${domainsSplit[1]}`
  setFieldValue('server', `${domain}:3030`)
})


function onInvalidSubmit({ values, errors, results }) {
  console.log('invalid!!')
  console.log(values) // current form values
  console.log(errors) // a map of field names and their first error message
  console.log(results) // a detailed map of field names and their validation results
}
const submit = handleSubmit(async (values) => {
  const api = useApiStore()
  console.log(`connecting to: ${server.value.value}`)
  api.create({ url: server.value.value, type: 'web' })

  const { username, password } = values
  const authStore = useAuthStore()
  const { user, error } = await authStore.login(username, password)

  if (error) {
    console.warn(error)
  }
  if (user) {
    router.push({
      name: 'Home',
    })
  }
}, onInvalidSubmit)
</script>
