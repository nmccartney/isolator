import { defineStore } from 'pinia'
import { useAlertStore } from '@/store/alert'
import { useUsersStore } from '@/store/users'
import { useApiStore } from '@/store/api'

export const useSampleStore = defineStore({
  id: 'sample',
  state: () => ({
    samples: [],
  }),
  getters: {
  },
  actions: {
    async getSamples() {
      try {
        const api = useApiStore()
        const { data } = await api.get(`/samples`)
        if (!data) throw Error({ reponse: { data: { message: 'no data provided in response' } } })
        this.samples = data.results
        return { samples: data.results }
      } catch (error) {
        console.warn(error)
        const { response } = error
        const errorMessage = response?.data?.message || 'Cannot get samples'
        const alertStore = useAlertStore()
        alertStore.error(errorMessage)
        return { error: errorMessage }
      }
    },
    async getNewSample(sample) {
      // if (!sample) throw Error('No sample given')
      try {
        const api = useApiStore()
        const { data } = await api.post(`/samples`, sample, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        console.log('created sample ', data)
        const alertStore = useAlertStore()
        alertStore.success('Request created!')
        await this.getSamples()
        return { sample: data }
      } catch (error) {
        console.warn(error)
        const { response } = error
        const errorMessage = response.data.message
        const alertStore = useAlertStore()
        alertStore.error(errorMessage)
        return { error: errorMessage }
      }
    },
    async getSampleById({ id }) {
      if (!id) throw Error('No sample id given')
      try {
        const api = useApiStore()
        const { data } = await api.get(`/samples/${id}`)
        return { sample: data }
      } catch (error) {
        console.warn(error)
        const { response } = error
        const errorMessage = response.data.message
        const alertStore = useAlertStore()
        alertStore.error(errorMessage)
        return { error: errorMessage }
      }
    },
    async updateSampleById({ id, sample }) {
      if (!sample) throw Error('No sample id given')

      try {
        const api = useApiStore()
        const { data } = await api.patch(`/samples/${id}`, sample)
        await this.getSamples()
        return { sample: data }
      } catch (error) {
        console.warn(error)
        const { response } = error
        const errorMessage = response.data.message
        const alertStore = useAlertStore()
        alertStore.error(errorMessage)
        return { error: errorMessage }
      }
    },
    async deleteSamplesById({ id }) {
      if (!id) throw Error('No sample id given')
      try {
        const api = useApiStore()
        const { data } = await api.delete(`/samples/${id}`)
        const alertStore = useAlertStore()
        alertStore.success('Deleted')
        await this.getSamples()
        return { sample: id }
      } catch (error) {
        console.warn(error)
        const { response } = error
        const errorMessage = response.data.message
        const alertStore = useAlertStore()
        alertStore.error(errorMessage)
        return { error: errorMessage }
      }
    },
  },
})
