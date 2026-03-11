import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import client from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  const user       = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const companyId  = ref(localStorage.getItem('company_id') || null)
  const tenantSlug = ref(localStorage.getItem('tenant_slug') || null)

  const isAuthenticated = computed(() => !!user.value)

  async function login(email, password) {
    const { data } = await client.post('/auth/login/', { email, password })
    localStorage.setItem('access_token',  data.access)
    localStorage.setItem('refresh_token', data.refresh)
    localStorage.setItem('user',          JSON.stringify(data.user))
    user.value = data.user

    // Load company and tenant automatically
    try {
      const compRes = await client.get('/accounts/companies/')
      const companies = compRes.data.results || compRes.data
      if (companies.length > 0) {
        const company = companies[0]
        localStorage.setItem('company_id',  company.id)
        localStorage.setItem('tenant_slug', company.tenant_slug || '')
        companyId.value  = company.id
        tenantSlug.value = company.tenant_slug || ''

        // Try to get tenant slug from tenant
        if (!company.tenant_slug && company.tenant) {
          const tenantRes = await client.get('/accounts/tenants/')
          const tenants = tenantRes.data.results || tenantRes.data
          const tenant = tenants.find(t => t.id === company.tenant)
          if (tenant) {
            localStorage.setItem('tenant_slug', tenant.slug)
            tenantSlug.value = tenant.slug
          }
        }
      }
    } catch {}

    return data
  }

  function setCompany(id, slug) {
    companyId.value  = id
    tenantSlug.value = slug
    localStorage.setItem('company_id',  id)
    localStorage.setItem('tenant_slug', slug)
  }

  function logout() {
    localStorage.clear()
    user.value       = null
    companyId.value  = null
    tenantSlug.value = null
    window.location.href = '/login'
  }

  return { user, companyId, tenantSlug, isAuthenticated, login, setCompany, logout }
})
