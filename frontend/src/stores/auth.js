import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import client from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  const user      = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const companyId = ref(localStorage.getItem('company_id') || null)

  const isAuthenticated = computed(() => !!user.value)

  async function login(email, password) {
    const { data } = await client.post('/auth/login/', { email, password })

    localStorage.setItem('access_token',  data.access)
    localStorage.setItem('refresh_token', data.refresh)
    localStorage.setItem('user',          JSON.stringify(data.user))

    user.value = data.user
    return data
  }

  function setCompany(id) {
    companyId.value = id
    localStorage.setItem('company_id', id)
  }

  function logout() {
    localStorage.clear()
    user.value      = null
    companyId.value = null
    window.location.href = '/login'
  }

  return { user, companyId, isAuthenticated, login, setCompany, logout }
})