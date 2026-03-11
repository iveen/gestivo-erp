import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor — inject token and company header
client.interceptors.request.use(config => {
  const token     = localStorage.getItem('access_token')
  const companyId = localStorage.getItem('company_id')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  if (companyId) {
    config.headers['X-Company-ID'] = companyId
  }
  const tenantSlug = localStorage.getItem('tenant_slug')
  if (tenantSlug) {
    config.headers['X-Tenant-Slug'] = tenantSlug
  }
  return config
})

// Response interceptor — handle 401 and refresh token
client.interceptors.response.use(
  response => response,
  async error => {
    const original = error.config

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      const refreshToken = localStorage.getItem('refresh_token')

      if (refreshToken) {
        try {
          const { data } = await axios.post('/api/auth/refresh/', {
            refresh: refreshToken
          })
          localStorage.setItem('access_token', data.access)
          original.headers.Authorization = `Bearer ${data.access}`
          return client(original)
        } catch {
          localStorage.clear()
          window.location.href = '/login'
        }
      } else {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default client