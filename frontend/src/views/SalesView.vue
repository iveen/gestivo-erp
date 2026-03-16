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

    <!-- ── CUSTOMERS ── -->
    <div v-if="activeTab === 'Customers'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Customers</h3>
        <button @click="openCustomerModal()"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Customer
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
            <tr v-if="customers.length === 0">
              <td colspan="6" class="px-4 py-6 text-center text-gray-400">No customers found</td>
            </tr>
            <tr v-for="c in customers" :key="c.id" class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 font-medium text-gray-800">{{ c.name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ c.email || '—' }}</td>
              <td class="px-4 py-3 text-gray-500">{{ c.phone || '—' }}</td>
              <td class="px-4 py-3 text-gray-500">{{ c.currency }}</td>
              <td class="px-4 py-3 text-right text-gray-600">{{ c.payment_terms }} days</td>
              <td class="px-4 py-3 space-x-3">
                <button @click="openCustomerModal(c)" class="text-xs text-blue-600 hover:underline">Edit</button>
                <button @click="deleteCustomer(c.id)" class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── QUOTATIONS ── -->
    <div v-if="activeTab === 'Quotations'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Quotations</h3>
        <button @click="openQuotationForm()"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Quotation
        </button>
      </div>

      <!-- Quotation Form -->
      <div v-if="showQuotationForm" class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6 space-y-4">
        <h4 class="text-sm font-semibold text-gray-700">New Quotation</h4>
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Customer *</label>
            <select v-model="quotationForm.customer" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm">
              <option value="">Select Customer</option>
              <option v-for="c in customers" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Date *</label>
            <input v-model="quotationForm.quotation_date" type="date" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Expiry Date</label>
            <input v-model="quotationForm.expiry_date" type="date" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Currency</label>
            <input v-model="quotationForm.currency" placeholder="USD" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Notes</label>
            <input v-model="quotationForm.notes" placeholder="Optional" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
        </div>

        <!-- Lines -->
        <div>
          <div class="flex justify-between items-center mb-2">
            <label class="text-xs text-gray-500">Order Lines</label>
            <button @click="addQuotationLine()" class="text-xs text-blue-600 hover:underline">+ Add Line</button>
          </div>
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
              <tr>
                <th class="text-left px-3 py-2">Product</th>
                <th class="text-left px-3 py-2">Description</th>
                <th class="text-right px-3 py-2">Qty</th>
                <th class="text-right px-3 py-2">Unit Price</th>
                <th class="text-right px-3 py-2">Discount %</th>
                <th class="text-right px-3 py-2">Subtotal</th>
                <th class="px-3 py-2"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(line, i) in quotationForm.lines" :key="i" class="border-t border-gray-50">
                <td class="px-2 py-1">
                  <select v-model="line.product" style="color:#111827"
                    class="w-full border border-gray-200 rounded px-2 py-1 text-sm"
                    @change="fillLineFromProduct(line)">
                    <option value="">Select Product</option>
                    <option v-for="p in sellableProducts" :key="p.id" :value="p.id">
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
                <td class="px-2 py-1">
                  <input v-model="line.discount" type="number" step="0.01" placeholder="0"
                    style="color:#111827"
                    class="w-20 border border-gray-200 rounded px-2 py-1 text-sm text-right" />
                </td>
                <td class="px-2 py-1 text-right text-gray-700 font-medium">
                  {{ fmt(lineSubtotal(line)) }}
                </td>
                <td class="px-2 py-1 text-center">
                  <button @click="removeQuotationLine(i)" class="text-red-400 hover:text-red-600 text-xs">✕</button>
                </td>
              </tr>
            </tbody>
            <tfoot class="border-t border-gray-200">
              <tr>
                <td colspan="5" class="px-3 py-2 text-right text-xs text-gray-500 font-semibold">Total</td>
                <td class="px-3 py-2 text-right text-sm font-bold text-gray-800">{{ fmt(quotationTotal) }}</td>
                <td></td>
              </tr>
            </tfoot>
          </table>
        </div>

        <p v-if="quotationError" class="text-xs text-red-500">{{ quotationError }}</p>
        <div class="flex justify-end gap-3">
          <button @click="showQuotationForm = false" class="text-sm text-gray-500 px-4 py-2">Cancel</button>
          <button @click="saveQuotation('draft')"
            class="border border-gray-300 text-gray-700 text-sm px-4 py-2 rounded-lg hover:bg-gray-50">
            Save as Draft
          </button>
          <button @click="saveQuotation('sent')"
            class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
            Send Quotation
          </button>
        </div>
      </div>

      <!-- Quotations List -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Customer</th>
              <th class="text-left px-4 py-3">Date</th>
              <th class="text-left px-4 py-3">Expiry</th>
              <th class="text-right px-4 py-3">Total</th>
              <th class="text-left px-4 py-3">Status</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="quotations.length === 0">
              <td colspan="6" class="px-4 py-6 text-center text-gray-400">No quotations found</td>
            </tr>
            <tr v-for="q in quotations" :key="q.id" class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 font-medium text-gray-800">{{ q.customer_name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ q.quotation_date }}</td>
              <td class="px-4 py-3 text-gray-500">{{ q.expiry_date || '—' }}</td>
              <td class="px-4 py-3 text-right font-medium text-gray-800">{{ fmt(q.total) }}</td>
              <td class="px-4 py-3">
                <span :class="statusClass(q.status)"
                  class="px-2 py-1 rounded-full text-xs font-medium capitalize">
                  {{ q.status }}
                </span>
              </td>
              <td class="px-4 py-3 space-x-2">
                <button @click="viewQuotation(q)" class="text-xs text-blue-600 hover:underline">View</button>
                <button v-if="q.status === 'draft'" @click="sendQuotation(q.id)"
                  class="text-xs text-yellow-600 hover:underline">Send</button>
                <button v-if="q.status === 'sent'" @click="confirmQuotation(q.id)"
                  class="text-xs text-green-600 hover:underline">Confirm</button>
                <button v-if="q.status === 'draft'" @click="deleteQuotation(q.id)"
                  class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── ORDERS ── -->
    <div v-if="activeTab === 'Orders'">
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Customer</th>
              <th class="text-left px-4 py-3">Order Date</th>
              <th class="text-right px-4 py-3">Total</th>
              <th class="text-left px-4 py-3">Status</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="orders.length === 0">
              <td colspan="5" class="px-4 py-6 text-center text-gray-400">No orders found</td>
            </tr>
            <tr v-for="o in orders" :key="o.id" class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 font-medium text-gray-800">{{ o.customer_name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ o.order_date }}</td>
              <td class="px-4 py-3 text-right font-medium text-gray-800">{{ fmt(o.total) }}</td>
              <td class="px-4 py-3">
                <span :class="statusClass(o.status)"
                  class="px-2 py-1 rounded-full text-xs font-medium capitalize">
                  {{ o.status.replace('_', ' ') }}
                </span>
              </td>
              <td class="px-4 py-3">
                <button @click="viewOrder(o)" class="text-xs text-blue-600 hover:underline">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── QUOTATION DETAIL MODAL ── -->
    <div v-if="selectedQuotation" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-2xl p-6 space-y-4">
        <div class="flex justify-between items-center">
          <h3 class="text-base font-semibold text-gray-800">Quotation</h3>
          <button @click="selectedQuotation = null" class="text-gray-400 hover:text-gray-600">✕</button>
        </div>
        <div class="grid grid-cols-3 gap-4 text-sm">
          <div><span class="text-gray-400 text-xs">Customer</span><p class="font-medium text-gray-800">{{ selectedQuotation.customer_name }}</p></div>
          <div><span class="text-gray-400 text-xs">Date</span><p class="font-medium text-gray-800">{{ selectedQuotation.quotation_date }}</p></div>
          <div><span class="text-gray-400 text-xs">Status</span>
            <span :class="statusClass(selectedQuotation.status)"
              class="px-2 py-1 rounded-full text-xs font-medium capitalize">
              {{ selectedQuotation.status }}
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
              <th class="text-right px-3 py-2">Disc %</th>
              <th class="text-right px-3 py-2">Subtotal</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="line in selectedQuotation.lines" :key="line.id" class="border-t border-gray-50">
              <td class="px-3 py-2 font-mono text-xs text-gray-500">{{ line.product_sku }}</td>
              <td class="px-3 py-2 text-gray-700">{{ line.product_name }}</td>
              <td class="px-3 py-2 text-right text-gray-700">{{ fmt(line.quantity) }}</td>
              <td class="px-3 py-2 text-right text-gray-700">{{ fmt(line.unit_price) }}</td>
              <td class="px-3 py-2 text-right text-gray-500">{{ line.discount }}%</td>
              <td class="px-3 py-2 text-right font-medium text-gray-800">{{ fmt(line.subtotal) }}</td>
            </tr>
          </tbody>
          <tfoot class="border-t-2 border-gray-200">
            <tr>
              <td colspan="5" class="px-3 py-2 text-right text-sm font-semibold text-gray-700">Total</td>
              <td class="px-3 py-2 text-right text-sm font-bold text-gray-800">{{ fmt(selectedQuotation.total) }}</td>
            </tr>
          </tfoot>
        </table>
        <div class="flex justify-end gap-3">
          <button v-if="selectedQuotation.status === 'draft'"
            @click="sendQuotation(selectedQuotation.id); selectedQuotation = null"
            class="border border-yellow-500 text-yellow-600 text-sm px-4 py-2 rounded-lg hover:bg-yellow-50">
            Send
          </button>
          <button v-if="selectedQuotation.status === 'sent'"
            @click="confirmQuotation(selectedQuotation.id); selectedQuotation = null"
            class="bg-green-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-green-700">
            Confirm Order
          </button>
          <button @click="selectedQuotation = null" class="text-sm text-gray-500 px-4 py-2">Close</button>
        </div>
      </div>
    </div>

    <!-- ── ORDER DETAIL MODAL ── -->
    <div v-if="selectedOrder" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6 space-y-4">
        <div class="flex justify-between items-center">
          <h3 class="text-base font-semibold text-gray-800">Sales Order</h3>
          <button @click="selectedOrder = null" class="text-gray-400 hover:text-gray-600">✕</button>
        </div>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div><span class="text-gray-400 text-xs">Customer</span><p class="font-medium text-gray-800">{{ selectedOrder.customer_name }}</p></div>
          <div><span class="text-gray-400 text-xs">Order Date</span><p class="font-medium text-gray-800">{{ selectedOrder.order_date }}</p></div>
        </div>
        <div class="flex justify-between items-center border-t pt-4">
          <span class="text-sm font-semibold text-gray-700">Total</span>
          <span class="text-base font-bold text-gray-800">{{ fmt(selectedOrder.total) }}</span>
        </div>
        <div class="flex justify-between items-center">
          <span :class="statusClass(selectedOrder.status)"
            class="px-3 py-1 rounded-full text-xs font-medium capitalize">
            {{ selectedOrder.status.replace('_', ' ') }}
          </span>
          <button @click="selectedOrder = null" class="text-sm text-gray-500 px-4 py-2">Close</button>
        </div>
      </div>
    </div>

    <!-- ── CUSTOMER MODAL ── -->
    <div v-if="customerModal.open" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 space-y-3">
        <h3 class="text-base font-semibold text-gray-800">{{ customerModal.editing ? 'Edit Customer' : 'New Customer' }}</h3>
        <input v-model="customerForm.name" placeholder="Name *" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        <input v-model="customerForm.email" placeholder="Email" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        <input v-model="customerForm.phone" placeholder="Phone" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        <input v-model="customerForm.tax_id" placeholder="Tax ID" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        <div class="grid grid-cols-2 gap-3">
          <input v-model="customerForm.currency" placeholder="Currency (USD)" style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          <input v-model="customerForm.payment_terms" type="number" placeholder="Payment Terms (days)"
            style="color:#111827" class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        </div>
        <textarea v-model="customerForm.address" placeholder="Address" rows="2" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm"></textarea>
        <p v-if="customerModal.error" class="text-xs text-red-500">{{ customerModal.error }}</p>
        <div class="flex justify-end gap-3">
          <button @click="customerModal.open = false" class="text-sm text-gray-500 px-4 py-2">Cancel</button>
          <button @click="saveCustomer"
            class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
            {{ customerModal.editing ? 'Save' : 'Create' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import client from '../api/client'

const activeTab  = ref('Customers')
const tabs       = ['Customers', 'Quotations', 'Orders']

const customers  = ref([])
const quotations = ref([])
const orders     = ref([])
const products   = ref([])

// Quotation form
const showQuotationForm = ref(false)
const quotationError    = ref('')
const selectedQuotation = ref(null)
const selectedOrder     = ref(null)
const quotationForm     = ref({ customer: '', quotation_date: '', expiry_date: '', currency: 'USD', notes: '', lines: [] })

// Customer modal
const customerModal = ref({ open: false, editing: false, id: null, error: '' })
const customerForm  = ref({})

// Helpers
function fmt(val) {
  return Number(val || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function statusClass(status) {
  const map = {
    draft:      'bg-gray-100 text-gray-600',
    sent:       'bg-blue-100 text-blue-700',
    confirmed:  'bg-green-100 text-green-700',
    cancelled:  'bg-red-100 text-red-600',
    in_delivery:'bg-yellow-100 text-yellow-700',
    done:       'bg-green-100 text-green-700',
  }
  return map[status] || 'bg-gray-100 text-gray-600'
}

const sellableProducts = computed(() => products.value.filter(p => p.can_be_sold))

function lineSubtotal(line) {
  const qty   = parseFloat(line.quantity)   || 0
  const price = parseFloat(line.unit_price) || 0
  const disc  = parseFloat(line.discount)   || 0
  return qty * price * (1 - disc / 100)
}

const quotationTotal = computed(() =>
  quotationForm.value.lines.reduce((s, l) => s + lineSubtotal(l), 0)
)

// Quotation
function openQuotationForm() {
  quotationError.value = ''
  quotationForm.value = {
    customer: customers.value[0]?.id || '',
    quotation_date: new Date().toISOString().slice(0, 10),
    expiry_date: '',
    currency: 'USD',
    notes: '',
    lines: [{ product: '', description: '', quantity: '', unit_price: '', discount: 0 }]
  }
  showQuotationForm.value = true
}

function addQuotationLine() {
  quotationForm.value.lines.push({ product: '', description: '', quantity: '', unit_price: '', discount: 0 })
}

function removeQuotationLine(i) {
  quotationForm.value.lines.splice(i, 1)
}

function fillLineFromProduct(line) {
  const p = products.value.find(p => p.id === line.product)
  if (p) {
    line.description = p.name
    line.unit_price  = p.sales_price
  }
}

async function saveQuotation(sendStatus) {
  quotationError.value = ''
  if (!quotationForm.value.customer)     { quotationError.value = 'Select a customer'; return }
  if (!quotationForm.value.quotation_date) { quotationError.value = 'Select a date'; return }
  if (quotationForm.value.lines.length === 0) { quotationError.value = 'Add at least one line'; return }
  try {
    const salesperson = JSON.parse(localStorage.getItem('user_id') || 'null')
    const payload = {
      customer:       quotationForm.value.customer,
      quotation_date: quotationForm.value.quotation_date,
      expiry_date:    quotationForm.value.expiry_date || null,
      currency:       quotationForm.value.currency,
      notes:          quotationForm.value.notes,
      salesperson:    salesperson,
      lines: quotationForm.value.lines.map(l => ({
        product:     l.product,
        description: l.description,
        quantity:    parseFloat(l.quantity)   || 0,
        unit_price:  parseFloat(l.unit_price) || 0,
        discount:    parseFloat(l.discount)   || 0,
      }))
    }
    const res = await client.post('/sales/quotations/', payload)
    // If "Send", immediately patch status to sent
    if (sendStatus === 'sent') {
      await client.post(`/sales/quotations/${res.data.id}/send_quotation/`)
    }
    showQuotationForm.value = false
    loadQuotations()
  } catch (e) {
    quotationError.value = JSON.stringify(e.response?.data || 'Error saving quotation')
  }
}

async function sendQuotation(id) {
  try {
    await client.post(`/sales/quotations/${id}/send_quotation/`)
    loadQuotations()
  } catch {}
}

async function confirmQuotation(id) {
  try {
    await client.post(`/sales/quotations/${id}/confirm/`)
    loadQuotations()
    loadOrders()
  } catch {}
}

async function deleteQuotation(id) {
  if (!confirm('Delete this draft quotation?')) return
  try { await client.delete(`/sales/quotations/${id}/`); loadQuotations() } catch {}
}

async function viewQuotation(q) {
  try {
    const r = await client.get(`/sales/quotations/${q.id}/`)
    selectedQuotation.value = r.data
  } catch { selectedQuotation.value = q }
}

async function viewOrder(o) {
  try {
    const r = await client.get(`/sales/orders/${o.id}/`)
    selectedOrder.value = r.data
  } catch { selectedOrder.value = o }
}

// Customer CRUD
function openCustomerModal(c = null) {
  customerModal.value = { open: true, editing: !!c, id: c?.id, error: '' }
  customerForm.value  = c ? { ...c } : { name: '', email: '', phone: '', tax_id: '', currency: 'USD', payment_terms: 30, address: '' }
}

async function saveCustomer() {
  try {
    if (customerModal.value.editing) {
      await client.patch(`/contacts/${customerModal.value.id}/`, customerForm.value)
    } else {
      await client.post('/contacts/', { ...customerForm.value, is_customer: true })
    }
    customerModal.value.open = false
    loadCustomers()
  } catch (e) {
    customerModal.value.error = JSON.stringify(e.response?.data || 'Error')
  }
}

async function deleteCustomer(id) {
  if (!confirm('Delete this customer?')) return
  try { await client.delete(`/contacts/${id}/`); loadCustomers() } catch {}
}

// Loaders
async function loadCustomers() {
  try { const r = await client.get('/contacts/?is_customer=true'); customers.value = r.data.results || r.data } catch {}
}
async function loadQuotations() {
  try { const r = await client.get('/sales/quotations/'); quotations.value = r.data.results || r.data } catch {}
}
async function loadOrders() {
  try { const r = await client.get('/sales/orders/'); orders.value = r.data.results || r.data } catch {}
}

onMounted(async () => {
  loadCustomers()
  loadQuotations()
  loadOrders()
  try {
    const r = await client.get('/inventory/products/?can_be_sold=true')
    products.value = r.data.results || r.data
  } catch {}

  // Store user id for salesperson field
  try {
    const r = await client.get('/accounts/users/me/')
    localStorage.setItem('user_id', JSON.stringify(r.data.id))
  } catch {}
})
</script>
