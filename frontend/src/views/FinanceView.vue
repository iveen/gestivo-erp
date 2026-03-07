<template>
  <div class="space-y-6">
    <!-- Tabs -->
    <div class="border-b border-gray-200">
      <nav class="flex space-x-6">
        <button
          v-for="tab in tabs" :key="tab"
          @click="activeTab = tab"
          class="pb-3 text-sm font-medium transition border-b-2"
          :class="activeTab === tab
            ? 'border-blue-600 text-blue-600'
            : 'border-transparent text-gray-500 hover:text-gray-700'"
        >
          {{ tab }}
        </button>
      </nav>
    </div>

    <!-- Chart of Accounts -->
    <div v-if="activeTab === 'Chart of Accounts'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Accounts</h3>
        <button class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Account
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Code</th>
              <th class="text-left px-4 py-3">Name</th>
              <th class="text-left px-4 py-3">Type</th>
              <th class="text-left px-4 py-3">Normal Balance</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="accounts.length === 0">
              <td colspan="4" class="px-4 py-6 text-center text-gray-400">No accounts found</td>
            </tr>
            <tr v-for="account in accounts" :key="account.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 font-mono text-gray-600">{{ account.code }}</td>
              <td class="px-4 py-3 text-gray-800">{{ account.name }}</td>
              <td class="px-4 py-3 text-gray-500 capitalize">{{ account.account_type }}</td>
              <td class="px-4 py-3 text-gray-500 capitalize">{{ account.normal_balance }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Journal Entries -->
    <div v-if="activeTab === 'Journal Entries'">
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Date</th>
              <th class="text-left px-4 py-3">Reference</th>
              <th class="text-left px-4 py-3">Journal</th>
              <th class="text-left px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="entries.length === 0">
              <td colspan="4" class="px-4 py-6 text-center text-gray-400">No journal entries found</td>
            </tr>
            <tr v-for="entry in entries" :key="entry.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-600">{{ entry.date }}</td>
              <td class="px-4 py-3 text-gray-800">{{ entry.reference }}</td>
              <td class="px-4 py-3 text-gray-500">{{ entry.journal }}</td>
              <td class="px-4 py-3">
                <span :class="entry.is_posted ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
                  class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ entry.is_posted ? 'Posted' : 'Draft' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Reports -->
    <div v-if="activeTab === 'Reports'">
      <div class="grid grid-cols-2 gap-4">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <h3 class="text-sm font-semibold text-gray-700 mb-3">Balance Sheet</h3>
          <p class="text-xs text-gray-400">Select a company to view the balance sheet.</p>
        </div>
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <h3 class="text-sm font-semibold text-gray-700 mb-3">Profit & Loss</h3>
          <p class="text-xs text-gray-400">Select a date range to view P&L.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import client from '../api/client'

const activeTab = ref('Chart of Accounts')
const tabs      = ['Chart of Accounts', 'Journal Entries', 'Reports']
const accounts  = ref([])
const entries   = ref([])

onMounted(async () => {
  try {
    const res = await client.get('/finance/accounts/')
    accounts.value = res.data.results || res.data
  } catch {}

  try {
    const res = await client.get('/finance/journal-entries/')
    entries.value = res.data.results || res.data
  } catch {}
})
</script>