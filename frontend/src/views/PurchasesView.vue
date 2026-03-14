<template>
  <div class="space-y-6">
    <!-- Tabs -->
    <div class="border-b border-gray-200">
      <nav class="flex space-x-6">
        <button v-for="tab in tabs" :key="tab" @click="activeTab = tab"
          class="pb-3 text-sm font-medium transition border-b-2"
          :class="activeTab === tab ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'">
          {{ tab }}
        </button>
      </nav>
    </div>

    <!-- ── VENDORS ── -->
    <div v-if="activeTab === 'Vendors'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Vendors</h3>
        <button @click="openVendorModal()"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Vendor
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Name</th>
              <th class="text-left px-4 py-3">Email</th>
              <th class="text-left px-4 py-3">Phone</th>
              <th class="text-left px-4 py-3">Currency</th>
              <th class="text-right px-4 py-3">Payment Terms</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="vendors.length === 0">
              <td colspan="6" class="px-4 py-6 text-center text-gray-400">No vendors found</td>
            </tr>
            <tr v-for="v in vendors" :key="v.id" class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 font-medium text-gray-800">{{ v.name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ v.email || '—' }}</td>
              <td class="px-4 py-3 text-gray-500">{{ v.phone || '—' }}</td>
              <td class="px-4 py-3 text-gray-500">{{ v.currency }}</td>
              <td class="px-4 py-3 text-right text-gray-600">{{ v.payment_terms }} days</td>
              <td class="px-4 py-3 space-x-3">
                <button @click="openVendorModal(v)" class="text-xs text-blue-600 hover:underline">Edit</button>
                <button @click="deleteVendor(v.id)" class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── PRODUCTS ── -->
    <div v-if="activeTab === 'Products'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Products</h3>
        <button @click="openProductModal()"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Product
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">SKU</th>
              <th class="text-left px-4 py-3">Name</th>
              <th class="text-left px-4 py-3">Category</th>
              <th class="text-left px-4 py-3">UOM</th>
              <th class="text-right px-4 py-3">Cost</th>
              <th class="text-right px-4 py-3">Sales Price</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="products.length === 0">
              <td colspan="7" class="px-4 py-6 text-center text-gray-400">No products found</td>
            </tr>
            <tr v-for="p in products" :key="p.id" class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 font-mono text-xs text-gray-600">{{ p.sku }}</td>
              <td class="px-4 py-3 text-gray-800">{{ p.name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ categoryName(p.category) }}</td>
              <td class="px-4 py-3 text-gray-500">{{ uomName(p.uom) }}</td>
              <td class="px-4 py-3 text-right text-gray-700">{{ fmt(p.cost) }}</td>
              <td class="px-4 py-3 text-right text-gray-700">{{ fmt(p.sales_price) }}</td>
              <td class="px-4 py-3 space-x-3">
                <button @click="openProductModal(p)" class="text-xs text-blue-600 hover:underline">Edit</button>
                <button @click="deleteProduct(p.id)" class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── PURCHASE ORDERS ── -->
    <div v-if="activeTab === 'Orders'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Purchase Orders</h3>
        <button @click="openPOForm()"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Order
        </button>
      </div>

      <!-- PO Form -->
      <div v-if="showPOForm" class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6 space-y-4">
        <h4 class="text-sm font-semibold text-gray-700">New Purchase Order</h4>
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Vendor</label>
            <select v-model="poForm.vendor" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm">
              <option value="">Select Vendor</option>
              <option v-for="v in vendors" :key="v.id" :value="v.id">{{ v.name }}</option>
            </select>
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Order Date</label>
            <input v-model="poForm.order_date" type="date" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Expected Date</label>
            <input v-model="poForm.expected_date" type="date" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Currency</label>
            <input v-model="poForm.currency" placeholder="USD" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Notes</label>
            <input v-model="poForm.notes" placeholder="Optional notes" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
        </div>

        <!-- Lines -->
        <div>
          <div class="flex justify-between items-center mb-2">
            <label class="text-xs text-gray-500">Order Lines</label>
            <button @click="addPOLine()" class="text-xs text-blue-600 hover:underline">+ Add Line</button>
          </div>
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
              <tr>
                <th class="text-left px-3 py-2">Product</th>
                <th class="text-left px-3 py-2">Description</th>
                <th class="text-right px-3 py-2">Qty</th>
                <th class="text-right px-3 py-2">Unit Price</th>
                <th class="text-right px-3 py-2">Subtotal</th>
                <th class="px-3 py-2"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(line, i) in poForm.lines" :key="i" class="border-t border-gray-50">
                <td class="px-2 py-1">
                  <select v-model="line.product" style="color:#111827"
                    class="w-full border border-gray-200 rounded px-2 py-1 text-sm"
                    @change="fillLineFromProduct(line)">
                    <option value="">Select Product</option>
                    <option v-for="p in products" :key="p.id" :value="p.id">
                      {{ p.sku }} - {{ p.name }}
                    </option>
                  </select>
                </td>
                <td class="px-2 py-1">
                  <input v-model="line.description" placeholder="Description" style="color:#111827"
                    class="w-full border border-gray-200 rounded px-2 py-1 text-sm" />
                </td>
                <td class="px-2 py-1">
                  <input v-model="line.quantity" type="number" step="0.01" placeholder="0"
                    style="color:#111827"
                    class="w-24 border border-gray-200 rounded px-2 py-1 text-sm text-right" />
                </td>
                <td class="px-2 py-1">
                  <input v-model="line.unit_price" type="number" step="0.01" placeholder="0.00"
                    style="color:#111827"
                    class="w-28 border border-gray-200 rounded px-2 py-1 text-sm text-right" />
                </td>
                <td class="px-2 py-1 text-right text-gray-700 font-medium">
                  {{ fmt((parseFloat(line.quantity)||0) * (parseFloat(line.unit_price)||0)) }}
                </td>
                <td class="px-2 py-1 text-center">
                  <button @click="removePOLine(i)" class="text-red-400 hover:text-red-600 text-xs">✕</button>
                </td>
              </tr>
            </tbody>
            <tfoot class="border-t border-gray-200">
              <tr>
                <td colspan="4" class="px-3 py-2 text-right text-xs text-gray-500 font-semibold">Total</td>
                <td class="px-3 py-2 text-right text-sm font-bold text-gray-800">{{ fmt(poTotal) }}</td>
                <td></td>
              </tr>
            </tfoot>
          </table>
        </div>

        <p v-if="poError" class="text-xs text-red-500">{{ poError }}</p>
        <div class="flex justify-end gap-3">
          <button @click="showPOForm = false" class="text-sm text-gray-500 hover:text-gray-700 px-4 py-2">Cancel</button>
          <button @click="savePO"
            class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
            Save Order
          </button>
        </div>
      </div>

      <!-- PO List -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Vendor</th>
              <th class="text-left px-4 py-3">Order Date</th>
              <th class="text-left px-4 py-3">Expected</th>
              <th class="text-right px-4 py-3">Total</th>
              <th class="text-left px-4 py-3">Status</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="orders.length === 0">
              <td colspan="6" class="px-4 py-6 text-center text-gray-400">No purchase orders found</td>
            </tr>
            <tr v-for="o in orders" :key="o.id" class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 font-medium text-gray-800">{{ o.vendor_name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ o.order_date }}</td>
              <td class="px-4 py-3 text-gray-500">{{ o.expected_date || '—' }}</td>
              <td class="px-4 py-3 text-right text-gray-800 font-medium">{{ fmt(o.total) }}</td>
              <td class="px-4 py-3">
                <span :class="statusClass(o.status)"
                  class="px-2 py-1 rounded-full text-xs font-medium capitalize">
                  {{ o.status }}
                </span>
              </td>
              <td class="px-4 py-3 space-x-2">
                <button @click="viewPO(o)" class="text-xs text-blue-600 hover:underline">View</button>
                <button v-if="o.status === 'draft'" @click="submitOrder(o.id)"
                  class="text-xs text-yellow-600 hover:underline">Submit</button>
                <button v-if="o.status === 'pending'" @click="approveOrder(o.id)"
                  class="text-xs text-green-600 hover:underline">Approve</button>
                <button v-if="o.status === 'draft'" @click="deleteOrder(o.id)"
                  class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- PO Detail Modal -->
    <div v-if="selectedPO" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-2xl p-6 space-y-4">
        <div class="flex justify-between items-center">
          <h3 class="text-base font-semibold text-gray-800">Purchase Order</h3>
          <button @click="selectedPO = null" class="text-gray-400 hover:text-gray-600">✕</button>
        </div>
        <div class="grid grid-cols-3 gap-4 text-sm">
          <div><span class="text-gray-400 text-xs">Vendor</span><p class="font-medium text-gray-800">{{ selectedPO.vendor_name || '—' }}</p></div>
          <div><span class="text-gray-400 text-xs">Order Date</span><p class="font-medium text-gray-800">{{ selectedPO.order_date || '—' }}</p></div>
          <div><span class="text-gray-400 text-xs">Status</span>
            <span :class="statusClass(selectedPO.status)"
              class="px-2 py-1 rounded-full text-xs font-medium capitalize">
              {{ selectedPO.status }}
            </span>
          </div>
        </div>
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-3 py-2">SKU</th>
              <th class="text-left px-3 py-2">Product</th>
              <th class="text-right px-3 py-2">Qty</th>
              <th class="text-right px-3 py-2">Unit Price</th>
              <th class="text-right px-3 py-2">Subtotal</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="line in selectedPO.lines" :key="line.id" class="border-t border-gray-50">
              <td class="px-3 py-2 font-mono text-xs text-gray-500">{{ line.product_sku }}</td>
              <td class="px-3 py-2 text-gray-700">{{ line.product_name }}</td>
              <td class="px-3 py-2 text-right text-gray-700">{{ fmt(line.quantity) }}</td>
              <td class="px-3 py-2 text-right text-gray-700">{{ fmt(line.unit_price) }}</td>
              <td class="px-3 py-2 text-right font-medium text-gray-800">{{ fmt(line.subtotal) }}</td>
            </tr>
          </tbody>
          <tfoot class="border-t-2 border-gray-200">
            <tr>
              <td colspan="4" class="px-3 py-2 text-right text-sm font-semibold text-gray-700">Total</td>
              <td class="px-3 py-2 text-right text-sm font-bold text-gray-800">{{ fmt(selectedPO.total) }}</td>
            </tr>
          </tfoot>
        </table>
        <div class="flex justify-end gap-3">
          <button v-if="selectedPO.status === 'draft'" @click="submitOrder(selectedPO.id); selectedPO = null"
            class="border border-yellow-500 text-yellow-600 text-sm px-4 py-2 rounded-lg hover:bg-yellow-50">
            Submit for Approval
          </button>
          <button v-if="selectedPO.status === 'pending'" @click="approveOrder(selectedPO.id); selectedPO = null"
            class="bg-green-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-green-700">
            Approve
          </button>
          <button @click="selectedPO = null" class="text-sm text-gray-500 hover:text-gray-700 px-4 py-2">Close</button>
        </div>
      </div>
    </div>

    <!-- Vendor Modal -->
    <div v-if="vendorModal.open" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 space-y-3">
        <h3 class="text-base font-semibold text-gray-800">{{ vendorModal.editing ? 'Edit Vendor' : 'New Vendor' }}</h3>
        <input v-model="vendorForm.name" placeholder="Name *" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        <input v-model="vendorForm.email" placeholder="Email" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        <input v-model="vendorForm.phone" placeholder="Phone" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        <input v-model="vendorForm.tax_id" placeholder="Tax ID" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        <div class="grid grid-cols-2 gap-3">
          <input v-model="vendorForm.currency" placeholder="Currency (USD)" style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <input v-model="vendorForm.payment_terms" type="number" placeholder="Payment Terms (days)"
            style="color:#111827" class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        </div>
        <textarea v-model="vendorForm.address" placeholder="Address" rows="2" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm"></textarea>
        <p v-if="vendorModal.error" class="text-xs text-red-500">{{ vendorModal.error }}</p>
        <div class="flex justify-end gap-3">
          <button @click="vendorModal.open = false" class="text-sm text-gray-500 px-4 py-2">Cancel</button>
          <button @click="saveVendor"
            class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
            {{ vendorModal.editing ? 'Save' : 'Create' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Product Modal -->
    <div v-if="productModal.open" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6 space-y-3">
        <h3 class="text-base font-semibold text-gray-800">{{ productModal.editing ? 'Edit Product' : 'New Product' }}</h3>
        <div class="grid grid-cols-2 gap-3">
          <input v-model="productForm.name" placeholder="Name *" style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <input v-model="productForm.sku" placeholder="SKU *" style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <select v-model="productForm.category" style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm">
            <option value="">Select Category</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
          <select v-model="productForm.uom" style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm">
            <option value="">Select UOM</option>
            <option v-for="u in uoms" :key="u.id" :value="u.id">{{ u.name }} ({{ u.symbol }})</option>
          </select>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Cost Price</label>
            <input v-model="productForm.cost" type="number" step="0.01" placeholder="0.00"
              style="color:#111827" class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Sales Price</label>
            <input v-model="productForm.sales_price" type="number" step="0.01" placeholder="0.00"
              style="color:#111827" class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
        </div>
        <p class="text-xs text-gray-400">
          Missing categories or UOMs?
          <button @click="productModal.open = false; activeTab = 'Categories'" class="text-blue-600 hover:underline">
            Manage them here.
          </button>
        </p>
        <p v-if="productModal.error" class="text-xs text-red-500">{{ productModal.error }}</p>
        <div class="flex justify-end gap-3">
          <button @click="productModal.open = false" class="text-sm text-gray-500 px-4 py-2">Cancel</button>
          <button @click="saveProduct"
            class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
            {{ productModal.editing ? 'Save' : 'Create' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import client from '../api/client'

const activeTab = ref('Vendors')
const tabs      = ['Vendors', 'Orders']

// Data
const vendors    = ref([])
const products   = ref([])
const categories = ref([])
const uoms       = ref([])
const orders     = ref([])

// PO form
const showPOForm  = ref(false)
const poError     = ref('')
const selectedPO  = ref(null)
const poForm      = ref({ vendor: '', order_date: '', expected_date: '', currency: 'USD', notes: '', lines: [] })

// Vendor modal
const vendorModal = ref({ open: false, editing: false, id: null, error: '' })
const vendorForm  = ref({})

// Product modal
const productModal = ref({ open: false, editing: false, id: null, error: '' })
const productForm  = ref({})

// Helpers
function fmt(val) {
  return Number(val || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function statusClass(status) {
  const map = {
    draft:     'bg-gray-100 text-gray-600',
    pending:   'bg-yellow-100 text-yellow-700',
    approved:  'bg-green-100 text-green-700',
    received:  'bg-blue-100 text-blue-700',
    cancelled: 'bg-red-100 text-red-600',
  }
  return map[status] || 'bg-gray-100 text-gray-600'
}

function categoryName(id) {
  return categories.value.find(c => c.id === id)?.name || '—'
}

function uomName(id) {
  const u = uoms.value.find(u => u.id === id)
  return u ? `${u.name} (${u.symbol})` : '—'
}

// PO
const poTotal = computed(() =>
  poForm.value.lines.reduce((s, l) =>
    s + (parseFloat(l.quantity) || 0) * (parseFloat(l.unit_price) || 0), 0)
)

function openPOForm() {
  poError.value = ''
  poForm.value = {
    vendor: vendors.value[0]?.id || '',
    order_date: new Date().toISOString().slice(0, 10),
    expected_date: '',
    currency: 'USD',
    notes: '',
    lines: [{ product: '', description: '', quantity: '', unit_price: '' }]
  }
  showPOForm.value = true
}

function addPOLine() {
  poForm.value.lines.push({ product: '', description: '', quantity: '', unit_price: '' })
}

function removePOLine(i) {
  poForm.value.lines.splice(i, 1)
}

function fillLineFromProduct(line) {
  const p = products.value.find(p => p.id === line.product)
  if (p) {
    line.description = p.name
    line.unit_price  = p.cost
  }
}

async function savePO() {
  poError.value = ''
  if (!poForm.value.vendor)     { poError.value = 'Select a vendor'; return }
  if (!poForm.value.order_date) { poError.value = 'Select a date'; return }
  if (poForm.value.lines.length === 0) { poError.value = 'Add at least one line'; return }
  try {
    await client.post('/purchases/orders/', {
      vendor:         poForm.value.vendor,
      order_date:     poForm.value.order_date,
      expected_date:  poForm.value.expected_date || null,
      currency:       poForm.value.currency,
      notes:          poForm.value.notes,
      lines: poForm.value.lines.map(l => ({
        product:     l.product,
        description: l.description,
        quantity:    parseFloat(l.quantity) || 0,
        unit_price:  parseFloat(l.unit_price) || 0,
      }))
    })
    showPOForm.value = false
    loadOrders()
  } catch (e) {
    poError.value = JSON.stringify(e.response?.data || 'Error saving PO')
  }
}

async function submitOrder(id) {
  try {
    await client.post(`/purchases/orders/${id}/submit/`)
    loadOrders()
  } catch {}
}

async function approveOrder(id) {
  try {
    await client.post(`/purchases/orders/${id}/approve/`)
    loadOrders()
  } catch {}
}

async function deleteOrder(id) {
  if (!confirm('Delete this draft order?')) return
  try {
    await client.delete(`/purchases/orders/${id}/`)
    loadOrders()
  } catch {}
}

async function viewPO(po) {
  try {
    const r = await client.get(`/purchases/orders/${po.id}/`)
    selectedPO.value = r.data
  } catch {
    selectedPO.value = po
  }
}

// Vendor CRUD
function openVendorModal(v = null) {
  vendorModal.value = { open: true, editing: !!v, id: v?.id, error: '' }
  vendorForm.value  = v ? { ...v } : { name: '', email: '', phone: '', tax_id: '', currency: 'USD', payment_terms: 30, address: '' }
}

async function saveVendor() {
  try {
    if (vendorModal.value.editing) {
      await client.patch(`/contacts/${vendorModal.value.id}/`, vendorForm.value)
    } else {
      await client.post('/contacts/', { ...vendorForm.value, is_vendor: true })
    }
    vendorModal.value.open = false
    loadVendors()
  } catch (e) {
    vendorModal.value.error = JSON.stringify(e.response?.data || 'Error')
  }
}

async function deleteVendor(id) {
  if (!confirm('Delete this vendor?')) return
  try { await client.delete(`/contacts/${id}/`); loadVendors() } catch {}
}

// Product CRUD
function openProductModal(p = null) {
  productModal.value = { open: true, editing: !!p, id: p?.id, error: '' }
  productForm.value  = p ? { ...p } : { name: '', sku: '', category: '', uom: '', cost: '', sales_price: '', valuation_method: 'average' }
}

async function saveProduct() {
  try {
    if (productModal.value.editing) {
      await client.patch(`/inventory/products/${productModal.value.id}/`, productForm.value)
    } else {
      await client.post('/inventory/products/', productForm.value)
    }
    productModal.value.open = false
    loadProducts()
  } catch (e) {
    productModal.value.error = JSON.stringify(e.response?.data || 'Error')
  }
}

async function deleteProduct(id) {
  if (!confirm('Delete this product?')) return
  try { await client.delete(`/inventory/products/${id}/`); loadProducts() } catch {}
}

// Loaders
async function loadVendors() {
  try { const r = await client.get('/contacts/?is_vendor=true'); vendors.value = r.data.results || r.data } catch {}
}
async function loadProducts() {
  try { const r = await client.get('/inventory/products/?can_be_purchased=true'); products.value = r.data.results || r.data } catch {}
}
async function loadOrders() {
  try { const r = await client.get('/purchases/orders/'); orders.value = r.data.results || r.data } catch {}
}

onMounted(async () => {
  loadVendors()
  loadProducts()
  loadOrders()
  try { const r = await client.get('/inventory/categories/'); categories.value = r.data.results || r.data } catch {}
  try { const r = await client.get('/inventory/uom/'); uoms.value = r.data.results || r.data } catch {}
})
</script>
