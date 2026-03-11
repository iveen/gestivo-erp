import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    component: () => import('../components/layout/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/DashboardView.vue'),
      },
      {
        path: 'finance',
        name: 'Finance',
        component: () => import('../views/FinanceView.vue'),
      },
      {
        path: 'inventory',
        name: 'Inventory',
        component: () => import('../views/InventoryView.vue'),
      },
      {
        path: 'sales',
        name: 'Sales',
        component: () => import('../views/SalesView.vue'),
      },
      {
        path: 'purchases',
        name: 'Purchases',
        component: () => import('../views/PurchasesView.vue'),
      },
      {
        path: 'manufacturing',
        name: 'Manufacturing',
        component: () => import('../views/ManufacturingView.vue'),
      },
      {
        path: 'crm',
        name: 'CRM',
        component: () => import('../views/CrmView.vue'),
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/SettingsView.vue'),
      meta: { requiresAuth: true }
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (!to.meta.public && !auth.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && auth.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router