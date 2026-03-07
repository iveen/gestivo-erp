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

    <!-- Products -->
    <div v-if="activeTab === 'Products'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Products</h3>
        <button class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Product
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">SKU</th>
              <th class="text-left px-4 py-3">Name</th>
              <th class="text-right px-4 py-3">Cost</th>
              <th class="text-right px-4 py-3">Sales Price</th>
              <th class="text-left px-4 py-3">Valuation</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="products.length === 0">
              <td colspan="5" class="px-4 py-6 text-center text-gray-400">No products found</td>
            </tr>
            <tr v-for="p in products" :key="p.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 font-mono text-gray-600">{{ p.sku }}</td>
              <td class="px-4 py-3 text-gray-800">{{ p.name }}</td>
              <td class="px-4 py-3 text-right text-gray-600">{{ p.cost }}</td>
              <td class="px-4 py-3 text-right text-gray-800 font-medium">{{ p.sales_price }}</td>
              <td class="px-4 py-3 text-gray-500 capitalize">{{ p.valuation_method }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Stock -->
    <div v-if="activeTab === 'Stock'">
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Product</th>
              <th class="text-left px-4 py-3">Location</th>
              <th class="text-right px-4 py-3">On Hand</th>
              <th class="text-right px-4 py-3">Reserved</th>
              <th class="text-right px-4 py-3">Available</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="quants.length === 0">
              <td colspan="5" class="px-4 py-6 text-center text-gray-400">No stock records found</td>
            </tr>
            <tr v-for="q in quants" :key="q.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-800">{{ q.product }}</td>
              <td class="px-4 py-3 text-gray-500">{{ q.location }}</td>
              <td class="px-4 py-3 text-right text-gray-800">{{ q.quantity }}</td>
              <td class="px-4 py-3 text-right text-gray-500">{{ q.reserved }}</td>
              <td class="px-4 py-3 text-right font-medium"
                :class="q.available_quantity > 0 ? 'text-green-600' : 'text-red-600'">
                {{ q.available_quantity }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Low Stock Alerts -->
    <div v-if="activeTab === 'Alerts'">
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">SKU</th>
              <th class="text-left px-4 py-3">Product</th>
              <th class="text-right px-4 py-3">On Hand</th>
              <th class="text-right px-4 py-3">Reorder Point</th>
              <th class="text-right px-4 py-3">Shortage</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="alerts.length === 0">
              <td colspan="5" class="px-4 py-6 text-center text-gray-400">No low stock alerts</td>
            </tr>
            <tr v-for="a in alerts" :key="a.sku"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 font-mono text-gray-600">{{ a.sku }}</td>
              <td class="px-4 py-3 text-gray-800">{{ a.product }}</td>
              <td class="px-4 py-3 text-right text-gray-600">{{ a.on_hand }}</td>
              <td class="px-4 py-3 text-right text-gray-500">{{ a.reorder_point }}</td>
              <td class="px-4 py-3 text-right text-red-600 font-medium">{{ a.shortage }}</td>
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

const activeTab = ref('Products')
const tabs      = ['Products', 'Stock', 'Alerts']
const products  = ref([])
const quants    = ref([])
const alerts    = ref([])

onMounted(async () => {
  try {
    const res = await client.get('/inventory/products/')
    products.value = res.data.results || res.data
  } catch {}

  try {
    const res = await client.get('/inventory/stock-quants/')
    quants.value = res.data.results || res.data
  } catch {}

  try {
    const res = await client.get('/inventory/low-stock/')
    alerts.value = res.data.results || res.data
  } catch {}
})
</script>