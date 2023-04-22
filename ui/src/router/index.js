// Composables
import { createRouter, createWebHistory } from 'vue-router'
// import Default from '@/layouts/default/Default.vue'
import Home from '@/views/Home.vue'
import Samples from '@/views/Samples.vue'

// let authStore = useAuthStore()

// TODO: figure out how to user authStore instead
const isAuthenticated = () => {
  return !!localStorage.getItem('user')
}

const gated = async (to, from) => {
  if (
    // make sure the user is authenticated
    (await !isAuthenticated()) &&
    // ❗️ Avoid an infinite redirect
    to.name !== 'login'
  ) {
    // redirect the user to the login page
    return { name: 'login' }
  }
}

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: Home, //() => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
        // beforeEnter: gated,
      },
      {
        path: 'samples',
        name: 'Samples',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: Samples, //() => import(/* webpackChunkName: "requests" */ '@/views/Requests.vue'),
        // beforeEnter: gated,
      },
    ],
  },
  {
    path: '/login',
    component: () => import('@/layouts/public/Default.vue'),
    children: [
      {
        path: '',
        name: 'login',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/views/Login.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
