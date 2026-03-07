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

    <!-- Manufacturing Orders -->
    <div v-if="activeTab === 'Orders'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Manufacturing Orders</h3>
        <button class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Order
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Product</th>
              <th class="text-right px-4 py-3">Quantity</th>
              <th class="text-left px-4 py-3">Scheduled</th>
              <th class="text-left px-4 py-3">Type</th>
              <th class="text-left px-4 py-3">State</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="orders.length === 0">
              <td colspan="6" class="px-4 py-6 text-center text-gray-400">No manufacturing orders found</td>
            </tr>
            <tr v-for="o in orders" :key="o.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-800">{{ o.product }}</td>
              <td class="px-4 py-3 text-right text-gray-600">{{ o.quantity }}</td>
              <td class="px-4 py-3 text-gray-500">{{ o.scheduled_date }}</td>
              <td class="px-4 py-3 text-gray-500 uppercase text-xs">{{ o.mo_type }}</td>
              <td class="px-4 py-3">
                <span :class="stateClass(o.state)"
                  class="px-2 py-1 rounded-full text-xs font-medium capitalize">
                  {{ o.state }}
                </span>
              </td>
              <td class="px-4 py-3">
                <button v-if="o.state === 'draft'"
                  @click="confirmOrder(o.id)"
                  class="text-xs text-blue-600 hover:underline">
                  Confirm
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- BOMs -->
    <div v-if="activeTab === 'Bill of Materials'">
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Product</th>
              <th class="text-left px-4 py-3">Version</th>
              <th class="text-right px-4 py-3">Quantity</th>
              <th class="text-left px-4 py-3">Type</th>
              <th class="text-right px-4 py-3">Components</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="boms.length === 0">
              <td colspan="5" class="px-4 py-6 text-center text-gray-400">No BOMs found</td>
            </tr>
            <tr v-for="b in boms" :key="b.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-800">{{ b.product }}</td>
              <td class="px-4 py-3 text-gray-500">{{ b.version }}</td>
              <td class="px-4 py-3 text-right text-gray-600">{{ b.quantity }}</td>
              <td class="px-4 py-3 text-gray-500 capitalize">{{ b.bom_type }}</td>
              <td class="px-4 py-3 text-right text-gray-600">{{ b.lines?.length || 0 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Work Centers -->
    <div v-if="activeTab === 'Work Centers'">
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Code</th>
              <th class="text-left px-4 py-3">Name</th>
              <th class="text-left px-4 py-3">Type</th>
              <th class="text-right px-4 py-3">Capacity</th>
              <th class="text-right px-4 py-3">Cost/Hour</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="workCenters.length === 0">
              <td colspan="5" class="px-4 py-6 text-center text-gray-400">No work centers found</td>
            </tr>
            <tr v-for="w in workCenters" :key="w.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 font-mono text-gray-600">{{ w.code }}</td>
              <td class="px-4 py-3 text-gray-800">{{ w.name }}</td>
              <td class="px-4 py-3 text-gray-500 capitalize">{{ w.center_type }}</td>
              <td class="px-4 py-3 text-right text-gray-600">{{ w.capacity }}</td>
              <td class="px-4 py-3 text-right text-gray-800">${{ w.cost_per_hour }}</td>
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

const activeTab  = ref('Orders')
const tabs       = ['Orders', 'Bill of Materials', 'Work Centers']
const orders     = ref([])
const boms       = ref([])
const workCenters = ref([])

function stateClass(state) {
  const map = {
    draft:       'bg-gray-100 text-gray-600',
    confirmed:   'bg-blue-100 text-blue-600',
    in_progress: 'bg-yellow-100 text-yellow-600',
    done:        'bg-green-100 text-green-600',
    cancelled:   'bg-red-100 text-red-600',
  }
  return map[state] || 'bg-gray-100 text-gray-600'
}

async function confirmOrder(id) {
  try {
    await client.post(`/manufacturing/orders/${id}/confirm/`)
    const res = await client.get('/manufacturing/orders/')
    orders.value = res.data.results || res.data
  } catch {}
}

onMounted(async () => {
  try {
    const res = await client.get('/manufacturing/orders/')
    orders.value = res.data.results || res.data
  } catch {}

  try {
    const res = await client.get('/manufacturing/boms/')
    boms.value = res.data.results || res.data
  } catch {}

  try {
    const res = await client.get('/manufacturing/work-centers/')
    workCenters.value = res.data.results || res.data
  } catch {}
})
</script>