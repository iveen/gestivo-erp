<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Sidebar -->
    <aside class="w-64 bg-blue-900 text-white flex flex-col">
      <div class="px-6 py-5 border-b border-blue-800">
        <h1 class="text-xl font-bold">Gestivo</h1>
        <p class="text-blue-300 text-xs mt-1">{{ auth.user?.full_name }}</p>
      </div>

      <nav class="flex-1 px-3 py-4 space-y-1">
        <SidebarItem to="/"            icon="home"          label="Dashboard"     />
        <SidebarItem to="/finance"     icon="currency"      label="Finance"       />
        <SidebarItem to="/inventory"   icon="cube"          label="Inventory"     />
        <SidebarItem to="/sales"       icon="shopping-cart" label="Sales"         />
        <SidebarItem to="/purchases"   icon="truck"         label="Purchases"     />
        <SidebarItem to="/manufacturing" icon="cog"         label="Manufacturing" />
        <SidebarItem to="/crm"         icon="users"         label="CRM"           />
      </nav>

      <div class="px-3 py-4 border-t border-blue-800">
        <button
          @click="auth.logout"
          class="w-full text-left px-3 py-2 text-blue-300 hover:text-white hover:bg-blue-800 rounded-lg text-sm transition"
        >
          Sign Out
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <header class="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-gray-800">{{ currentTitle }}</h2>
        <span class="text-sm text-gray-500">{{ today }}</span>
      </header>

      <main class="flex-1 overflow-y-auto p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import SidebarItem from './SidebarItem.vue'

const auth  = useAuthStore()
const route = useRoute()

const currentTitle = computed(() => route.name || 'Dashboard')
const today = computed(() => new Date().toLocaleDateString('en-US', {
  weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
}))
</script>