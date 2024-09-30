import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TranslationView from '../views/TranslationView.vue'
import PreviewView from '../views/PreviewView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/translation',
      name: 'translation',
      component: TranslationView
    },
    {
      path: '/preview',
      name: 'preview',
      component: PreviewView
    }
  ]
})

export default router
