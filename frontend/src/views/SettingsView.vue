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

    <!-- Tenants -->
    <div v-if="activeTab === 'Tenants'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Tenants</h3>
        <button @click="openModal('tenant')"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Tenant
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Name</th>
              <th class="text-left px-4 py-3">Slug</th>
              <th class="text-left px-4 py-3">Status</th>
              <th class="text-left px-4 py-3">Created</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="tenants.length === 0">
              <td colspan="5" class="px-4 py-6 text-center text-gray-400">No tenants found</td>
            </tr>
            <tr v-for="t in tenants" :key="t.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-800 font-medium">{{ t.name }}</td>
              <td class="px-4 py-3 font-mono text-gray-500">{{ t.slug }}</td>
              <td class="px-4 py-3">
                <span :class="t.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                  class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ t.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-4 py-3 text-gray-400">{{ t.created_at?.slice(0,10) }}</td>
              <td class="px-4 py-3 space-x-3">
                <button @click="editItem('tenant', t)"
                  class="text-xs text-blue-600 hover:underline">Edit</button>
                <button @click="deleteItem('tenants', t.id, loadTenants)"
                  class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Companies -->
    <div v-if="activeTab === 'Companies'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Companies</h3>
        <button @click="openModal('company')"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Company
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Name</th>
              <th class="text-left px-4 py-3">Legal Name</th>
              <th class="text-left px-4 py-3">Tax ID</th>
              <th class="text-left px-4 py-3">Currency</th>
              <th class="text-left px-4 py-3">Status</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="companies.length === 0">
              <td colspan="6" class="px-4 py-6 text-center text-gray-400">No companies found</td>
            </tr>
            <tr v-for="c in companies" :key="c.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-800 font-medium">{{ c.name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ c.legal_name }}</td>
              <td class="px-4 py-3 font-mono text-gray-500">{{ c.tax_id }}</td>
              <td class="px-4 py-3 text-gray-500">{{ c.currency }}</td>
              <td class="px-4 py-3">
                <span :class="c.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                  class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ c.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-4 py-3 space-x-3">
                <button @click="editItem('company', c)"
                  class="text-xs text-blue-600 hover:underline">Edit</button>
                <button @click="deleteItem('companies', c.id, loadCompanies)"
                  class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Users -->
    <div v-if="activeTab === 'Users'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Users</h3>
        <button @click="openModal('user')"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New User
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Name</th>
              <th class="text-left px-4 py-3">Email</th>
              <th class="text-left px-4 py-3">Status</th>
              <th class="text-left px-4 py-3">Staff</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="users.length === 0">
              <td colspan="5" class="px-4 py-6 text-center text-gray-400">No users found</td>
            </tr>
            <tr v-for="u in users" :key="u.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-800 font-medium">{{ u.full_name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ u.email }}</td>
              <td class="px-4 py-3">
                <span :class="u.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                  class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ u.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <span v-if="u.is_staff" class="bg-blue-100 text-blue-700 px-2 py-1 rounded-full text-xs">Staff</span>
                <span v-else class="text-gray-300 text-xs">—</span>
              </td>
              <td class="px-4 py-3 space-x-3">
                <button @click="editItem('user', u)"
                  class="text-xs text-blue-600 hover:underline">Edit</button>
                <button @click="deleteItem('users', u.id, loadUsers)"
                  class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Roles -->
    <div v-if="activeTab === 'Roles'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Roles</h3>
        <button @click="openModal('role')"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Role
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Name</th>
              <th class="text-left px-4 py-3">Description</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="roles.length === 0">
              <td colspan="3" class="px-4 py-6 text-center text-gray-400">No roles found</td>
            </tr>
            <tr v-for="r in roles" :key="r.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-800 font-medium">{{ r.name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ r.description || '—' }}</td>
              <td class="px-4 py-3 space-x-3">
                <button @click="editItem('role', r)"
                  class="text-xs text-blue-600 hover:underline">Edit</button>
                <button @click="deleteItem('roles', r.id, loadRoles)"
                  class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="modal.open"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 space-y-4">
        <h3 class="text-base font-semibold text-gray-800 capitalize">
          {{ modal.editing ? 'Edit' : 'New' }} {{ modal.type }}
        </h3>

        <!-- Tenant Form -->
        <template v-if="modal.type === 'tenant'">
          <input v-model="form.name" placeholder="Name"
            style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <input v-model="form.slug" placeholder="Slug (e.g. acme-corp)"
            style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <label class="flex items-center gap-2 text-sm text-gray-600">
            <input type="checkbox" v-model="form.is_active" /> Active
          </label>
        </template>

        <!-- Company Form -->
        <template v-if="modal.type === 'company'">
          <select v-model="form.tenant"
            style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm">
            <option value="">Select Tenant</option>
            <option v-for="t in tenants" :key="t.id" :value="t.id">{{ t.name }}</option>
          </select>
          <input v-model="form.name" placeholder="Name"
            style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <input v-model="form.legal_name" placeholder="Legal Name"
            style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <input v-model="form.tax_id" placeholder="Tax ID"
            style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <input v-model="form.currency" placeholder="Currency (e.g. USD)"
            style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <label class="flex items-center gap-2 text-sm text-gray-600">
            <input type="checkbox" v-model="form.is_active" /> Active
          </label>
        </template>

        <!-- User Form -->
        <template v-if="modal.type === 'user'">
          <input v-model="form.first_name" placeholder="First Name"
            style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <input v-model="form.last_name" placeholder="Last Name"
            style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <input v-model="form.email" placeholder="Email" type="email"
            style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <input v-model="form.password" placeholder="Password (leave blank to keep)"
            type="password" style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <label class="flex items-center gap-2 text-sm text-gray-600">
            <input type="checkbox" v-model="form.is_active" /> Active
          </label>
          <label class="flex items-center gap-2 text-sm text-gray-600">
            <input type="checkbox" v-model="form.is_staff" /> Staff
          </label>
        </template>

        <!-- Role Form -->
        <template v-if="modal.type === 'role'">
          <input v-model="form.name" placeholder="Role Name"
            style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <input v-model="form.description" placeholder="Description"
            style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        </template>

        <!-- Error -->
        <p v-if="modal.error" class="text-xs text-red-500">{{ modal.error }}</p>

        <!-- Buttons -->
        <div class="flex justify-end gap-3 pt-2">
          <button @click="modal.open = false"
            class="text-sm text-gray-500 hover:text-gray-700 px-4 py-2">
            Cancel
          </button>
          <button @click="saveItem"
            class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
            {{ modal.editing ? 'Save Changes' : 'Create' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import client from '../api/client'

const activeTab = ref('Tenants')
const tabs      = ['Tenants', 'Companies', 'Users', 'Roles']

const tenants   = ref([])
const companies = ref([])
const users     = ref([])
const roles     = ref([])

const modal = ref({ open: false, type: '', editing: false, id: null, error: '' })
const form  = ref({})

const endpointMap = {
  tenant:  'accounts/tenants',
  company: 'accounts/companies',
  user:    'accounts/users',
  role:    'accounts/roles',
}

async function loadTenants() {
  try {
    const res = await client.get('/accounts/tenants/')
    tenants.value = res.data.results || res.data
  } catch {}
}

async function loadCompanies() {
  try {
    const res = await client.get('/accounts/companies/')
    companies.value = res.data.results || res.data
  } catch {}
}

async function loadUsers() {
  try {
    const res = await client.get('/accounts/users/')
    users.value = res.data.results || res.data
  } catch {}
}

async function loadRoles() {
  try {
    const res = await client.get('/accounts/roles/')
    roles.value = res.data.results || res.data
  } catch {}
}

function openModal(type) {
  modal.value = { open: true, type, editing: false, id: null, error: '' }
  form.value  = { is_active: true }
}

function editItem(type, item) {
  modal.value = { open: true, type, editing: true, id: item.id, error: '' }
  form.value  = { ...item }
}

async function saveItem() {
  const endpoint = endpointMap[modal.value.type]
  try {
    const payload = { ...form.value }
    // Remove empty password on edit
    if (modal.value.editing && !payload.password) delete payload.password

    if (modal.value.editing) {
      await client.patch(`/${endpoint}/${modal.value.id}/`, payload)
    } else {
      await client.post(`/${endpoint}/`, payload)
    }
    modal.value.open = false
    // Reload the right list
    if (modal.value.type === 'tenant')  loadTenants()
    if (modal.value.type === 'company') loadCompanies()
    if (modal.value.type === 'user')    loadUsers()
    if (modal.value.type === 'role')    loadRoles()
  } catch (e) {
    modal.value.error = JSON.stringify(e.response?.data || 'Error saving')
  }
}

async function deleteItem(endpoint, id, reload) {
  if (!confirm('Are you sure you want to delete this item?')) return
  try {
    await client.delete(`/accounts/${endpoint}/${id}/`)
    reload()
  } catch {}
}

onMounted(() => {
  loadTenants()
  loadCompanies()
  loadUsers()
  loadRoles()
})
</script>