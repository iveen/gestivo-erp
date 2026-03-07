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

    <!-- Quotations -->
    <div v-if="activeTab === 'Quotations'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Quotations</h3>
        <button class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Quotation
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Customer</th>
              <th class="text-left px-4 py-3">Date</th>
              <th class="text-right px-4 py-3">Total</th>
              <th class="text-left px-4 py-3">Status</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="quotations.length === 0">
              <td colspan="5" class="px-4 py-6 text-center text-gray-400">No quotations found</td>
            </tr>
            <tr v-for="q in quotations" :key="q.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-800">{{ q.customer }}</td>
              <td class="px-4 py-3 text-gray-500">{{ q.quotation_date }}</td>
              <td class="px-4 py-3 text-right text-gray-800 font-medium">{{ q.total }}</td>
              <td class="px-4 py-3">
                <span :class="statusClass(q.status)"
                  class="px-2 py-1 rounded-full text-xs font-medium capitalize">
                  {{ q.status }}
                </span>
              </td>
              <td class="px-4 py-3">
                <button v-if="q.status === 'sent'"
                  @click="confirmQuotation(q.id)"
                  class="text-xs text-blue-600 hover:underline">
                  Confirm
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Orders -->
    <div v-if="activeTab === 'Orders'">
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Customer</th>
              <th class="text-left px-4 py-3">Date</th>
              <th class="text-right px-4 py-3">Total</th>
              <th class="text-left px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="orders.length === 0">
              <td colspan="4" class="px-4 py-6 text-center text-gray-400">No orders found</td>
            </tr>
            <tr v-for="o in orders" :key="o.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-800">{{ o.customer }}</td>
              <td class="px-4 py-3 text-gray-500">{{ o.order_date }}</td>
              <td class="px-4 py-3 text-right text-gray-800 font-medium">{{ o.total }}</td>
              <td class="px-4 py-3">
                <span :class="statusClass(o.status)"
                  class="px-2 py-1 rounded-full text-xs font-medium capitalize">
                  {{ o.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Customers -->
    <div v-if="activeTab === 'Customers'">
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Name</th>
              <th class="text-left px-4 py-3">Email</th>
              <th class="text-left px-4 py-3">Currency</th>
              <th class="text-right px-4 py-3">Credit Limit</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="customers.length === 0">
              <td colspan="4" class="px-4 py-6 text-center text-gray-400">No customers found</td>
            </tr>
            <tr v-for="c in customers" :key="c.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-800">{{ c.name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ c.email }}</td>
              <td class="px-4 py-3 text-gray-500">{{ c.currency }}</td>
              <td class="px-4 py-3 text-right text-gray-800">{{ c.credit_limit }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import client from '../api/client'

const activeTab  = ref('Quotations')
const tabs       = ['Quotations', 'Orders', 'Customers']
const quotations = ref([])
const orders     = ref([])
const customers  = ref([])

function statusClass(status) {
  const map = {
    draft:      'bg-gray-100 text-gray-600',
    sent:       'bg-blue-100 text-blue-600',
    confirmed:  'bg-green-100 text-green-600',
    cancelled:  'bg-red-100 text-red-600',
    in_delivery:'bg-yellow-100 text-yellow-600',
    done:       'bg-green-100 text-green-600',
  }
  return map[status] || 'bg-gray-100 text-gray-600'
}

async function confirmQuotation(id) {
  try {
    await client.post(`/sales/quotations/${id}/confirm/`)
    const res = await client.get('/sales/quotations/')
    quotations.value = res.data.results || res.data
  } catch {}
}

onMounted(async () => {
  try {
    const res = await client.get('/sales/quotations/')
    quotations.value = res.data.results || res.data
  } catch {}

  try {
    const res = await client.get('/sales/orders/')
    orders.value = res.data.results || res.data
  } catch {}

  try {
    const res = await client.get('/finance/customers/')
    customers.value = res.data.results || res.data
  } catch {}
})
</script>