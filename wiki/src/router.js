import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {path: '/', name: 'Home', component: () => import('@/pages/Home.vue'),},
  {path: '/edit', name: 'Edit', component: () => import('@/pages/Edit.vue'),},
  {path: '/detail/:pk', name: 'WikiDetail', component: () => import('@/pages/WikiDetail.vue'),},
]

let router = createRouter({
  history: createWebHistory('/one_wiki'),
  routes,
})

export default router
