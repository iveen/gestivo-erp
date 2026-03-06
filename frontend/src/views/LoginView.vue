<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center">
    <div class="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md">
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold text-blue-800">Gestivo</h1>
        <p class="text-gray-500 mt-1">Sign in to your account</p>
      </div>

      <div v-if="error" class="mb-4 p-3 bg-red-50 text-red-600 rounded-lg text-sm">
        {{ error }}
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="you@example.com"
            style="color: #111827;"
            class="w-full border border-gray-900 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            style="color: #111827;"
            class="w-full border border-gray-900 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          @click="handleLogin"
          :disabled="loading"
          class="w-full bg-blue-800 text-white rounded-lg py-2 font-medium hover:bg-blue-900 transition disabled:opacity-50"
        >
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router   = useRouter()
const auth     = useAuthStore()
const email    = ref('')
const password = ref('')
const loading  = ref(false)
const error    = ref('')

async function handleLogin() {
  loading.value = true
  error.value   = ''
  try {
    await auth.login(email.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = 'Invalid email or password.'
  } finally {
    loading.value = false
  }
}
</script>