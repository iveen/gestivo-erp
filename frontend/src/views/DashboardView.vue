<template>
  <div class="space-y-6">
    <!-- KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div v-for="kpi in kpis" :key="kpi.label"
        class="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
        <p class="text-sm text-gray-500">{{ kpi.label }}</p>
        <p class="text-2xl font-bold text-gray-800 mt-1">{{ kpi.value }}</p>
        <p :class="kpi.positive ? 'text-green-500' : 'text-red-500'"
          class="text-xs mt-1">{{ kpi.change }}</p>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
        <h3 class="text-sm font-semibold text-gray-700 mb-4">Monthly Revenue</h3>
        <canvas ref="revenueChart"></canvas>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
        <h3 class="text-sm font-semibold text-gray-700 mb-4">Expenses by Category</h3>
        <canvas ref="expenseChart"></canvas>
      </div>
    </div>

    <!-- Bottom Row -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
        <h3 class="text-sm font-semibold text-gray-700 mb-4">Sales Pipeline</h3>
        <div v-for="stage in pipeline" :key="stage.label" class="mb-3">
          <div class="flex justify-between text-xs text-gray-500 mb-1">
            <span>{{ stage.label }}</span>
            <span>{{ stage.value }}</span>
          </div>
          <div class="w-full bg-gray-100 rounded-full h-2">
            <div class="bg-blue-600 h-2 rounded-full"
              :style="{ width: stage.pct + '%' }"></div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
        <h3 class="text-sm font-semibold text-gray-700 mb-4">Top Products</h3>
        <table class="w-full text-sm">
          <thead>
            <tr class="text-gray-400 text-xs">
              <th class="text-left pb-2">Product</th>
              <th class="text-right pb-2">Units</th>
              <th class="text-right pb-2">Revenue</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in topProducts" :key="p.name" class="border-t border-gray-50">
              <td class="py-2 text-gray-700">{{ p.name }}</td>
              <td class="py-2 text-right text-gray-500">{{ p.units }}</td>
              <td class="py-2 text-right text-gray-800 font-medium">{{ p.revenue }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

const revenueChart = ref(null)
const expenseChart = ref(null)

const kpis = [
  { label: 'Total Revenue',  value: '$124,500', change: '+12% vs last month', positive: true  },
  { label: 'Total Expenses', value: '$87,200',  change: '+5% vs last month',  positive: false },
  { label: 'Open Tasks',     value: '24',       change: '3 due today',        positive: true  },
  { label: 'Net Income',     value: '$37,300',  change: '+18% vs last month', positive: true  },
]

const pipeline = [
  { label: 'New',         value: '$45,000', pct: 80 },
  { label: 'Qualified',   value: '$32,000', pct: 60 },
  { label: 'Proposition', value: '$18,000', pct: 40 },
  { label: 'Negotiation', value: '$9,000',  pct: 20 },
]

const topProducts = [
  { name: 'Product A', units: 145, revenue: '$28,000' },
  { name: 'Product B', units: 98,  revenue: '$19,600' },
  { name: 'Product C', units: 76,  revenue: '$15,200' },
  { name: 'Product D', units: 54,  revenue: '$10,800' },
]

onMounted(() => {
  new Chart(revenueChart.value, {
    type: 'bar',
    data: {
      labels: ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'],
      datasets: [{
        label: 'Revenue',
        data: [95000, 102000, 118000, 108000, 115000, 124500],
        backgroundColor: '#1565C0',
        borderRadius: 4,
      }]
    },
    options: { responsive: true, plugins: { legend: { display: false } } }
  })

  new Chart(expenseChart.value, {
    type: 'doughnut',
    data: {
      labels: ['Operations', 'Salaries', 'Marketing', 'Other'],
      datasets: [{
        data: [35000, 42000, 7200, 3000],
        backgroundColor: ['#1565C0', '#00695C', '#F57C00', '#9E9E9E'],
      }]
    },
    options: { responsive: true }
  })
})
</script>