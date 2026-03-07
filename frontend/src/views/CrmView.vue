<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-sm font-semibold text-gray-700">Sales Pipeline</h3>
      <button class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
        + New Lead
      </button>
    </div>

    <!-- Kanban Board -->
    <div class="flex gap-4 overflow-x-auto pb-4">
      <div
        v-for="stage in stages" :key="stage.key"
        class="flex-shrink-0 w-64"
      >
        <!-- Column Header -->
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">
            {{ stage.label }}
          </span>
          <span class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
            {{ leadsForStage(stage.key).length }}
          </span>
        </div>

        <!-- Cards -->
        <div class="space-y-3">
          <div
            v-for="lead in leadsForStage(stage.key)" :key="lead.id"
            class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 cursor-pointer hover:shadow-md transition"
          >
            <p class="text-sm font-medium text-gray-800">{{ lead.name }}</p>
            <p class="text-xs text-gray-400 mt-1">{{ lead.contact }}</p>
            <div class="flex justify-between items-center mt-3">
              <span class="text-xs font-semibold text-blue-700">
                ${{ Number(lead.expected_revenue).toLocaleString() }}
              </span>
              <span class="text-xs text-gray-400">{{ lead.probability }}%</span>
            </div>
            <div class="mt-2 w-full bg-gray-100 rounded-full h-1">
              <div
                class="bg-blue-500 h-1 rounded-full"
                :style="{ width: lead.probability + '%' }"
              ></div>
            </div>
          </div>

          <!-- Empty state -->
          <div v-if="leadsForStage(stage.key).length === 0"
            class="border-2 border-dashed border-gray-200 rounded-xl p-4 text-center">
            <p class="text-xs text-gray-300">No leads</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import client from '../api/client'

const leads = ref([])

const stages = [
  { key: 'new',         label: 'New'         },
  { key: 'qualified',   label: 'Qualified'   },
  { key: 'proposition', label: 'Proposition' },
  { key: 'negotiation', label: 'Negotiation' },
  { key: 'won',         label: 'Won'         },
  { key: 'lost',        label: 'Lost'        },
]

function leadsForStage(stage) {
  return leads.value.filter(l => l.stage === stage)
}

onMounted(async () => {
  try {
    const res = await client.get('/crm/leads/')
    leads.value = res.data.results || res.data
  } catch {}
})
</script>