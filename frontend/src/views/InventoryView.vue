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
              <th class="text-left px-4 py-3">Type</th>
              <th class="text-left px-4 py-3">Valuation</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="products.length === 0">
              <td colspan="8" class="px-4 py-6 text-center text-gray-400">No products found</td>
            </tr>
            <tr v-for="p in products" :key="p.id" class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 font-mono text-xs text-gray-600">{{ p.sku }}</td>
              <td class="px-4 py-3 text-gray-800 font-medium">{{ p.name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ categoryName(p.category) }}</td>
              <td class="px-4 py-3 text-gray-500">{{ uomSymbol(p.uom) }}</td>
              <td class="px-4 py-3 text-right text-gray-600">{{ fmt(p.cost) }}</td>
              <td class="px-4 py-3 text-right text-gray-800 font-medium">{{ fmt(p.sales_price) }}</td>
              <td class="px-4 py-3">
                <span :class="typeClass(p.product_type)" class="px-2 py-1 rounded-full text-xs font-medium capitalize">
                  {{ p.product_type }}
                </span>
              </td>
              <td class="px-4 py-3 text-gray-500 capitalize">{{ ['service','digital'].includes(p.product_type) ? '—' : p.valuation_method }}</td>
              <td class="px-4 py-3 space-x-3">
                <button @click="openProductModal(p)" class="text-xs text-blue-600 hover:underline">Edit</button>
                <button @click="deleteProduct(p.id)" class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── CATEGORIES ── -->
    <div v-if="activeTab === 'Categories'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Product Categories</h3>
        <button @click="openCategoryModal()"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Category
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Name</th>
              <th class="text-left px-4 py-3">Parent</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="categories.length === 0">
              <td colspan="3" class="px-4 py-6 text-center text-gray-400">No categories found</td>
            </tr>
            <tr v-for="c in categories" :key="c.id" class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-800">{{ c.name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ categoryName(c.parent) || '—' }}</td>
              <td class="px-4 py-3 space-x-3">
                <button @click="openCategoryModal(c)" class="text-xs text-blue-600 hover:underline">Edit</button>
                <button @click="deleteCategory(c.id)" class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── UNITS OF MEASURE ── -->
    <div v-if="activeTab === 'UOMs'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Units of Measure</h3>
        <button @click="openUomModal()"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New UOM
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Name</th>
              <th class="text-left px-4 py-3">Symbol</th>
              <th class="text-left px-4 py-3">Category</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="uoms.length === 0">
              <td colspan="4" class="px-4 py-6 text-center text-gray-400">No UOMs found</td>
            </tr>
            <tr v-for="u in uoms" :key="u.id" class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-800">{{ u.name }}</td>
              <td class="px-4 py-3 font-mono text-gray-600">{{ u.symbol }}</td>
              <td class="px-4 py-3 text-gray-500 capitalize">{{ u.category }}</td>
              <td class="px-4 py-3 space-x-3">
                <button @click="openUomModal(u)" class="text-xs text-blue-600 hover:underline">Edit</button>
                <button @click="deleteUom(u.id)" class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── STOCK ── -->
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
            <tr v-for="q in quants" :key="q.id" class="border-t border-gray-50 hover:bg-gray-50">
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

    <!-- ── LOW STOCK ALERTS ── -->
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
            <tr v-for="a in alerts" :key="a.sku" class="border-t border-gray-50 hover:bg-gray-50">
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

    <!-- ── PRODUCT MODAL ── -->
    <div v-if="productModal.open" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6 space-y-3">
        <h3 class="text-base font-semibold text-gray-800">{{ productModal.editing ? 'Edit Product' : 'New Product' }}</h3>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Name *</label>
            <input v-model="productForm.name" placeholder="Product name" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">SKU *</label>
            <input v-model="productForm.sku" placeholder="SKU-001" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Category *</label>
            <select v-model="productForm.category" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm">
              <option value="">Select Category</option>
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Unit of Measure *</label>
            <select v-model="productForm.uom" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm">
              <option value="">Select UOM</option>
              <option v-for="u in uoms" :key="u.id" :value="u.id">{{ u.name }} ({{ u.symbol }})</option>
            </select>
          </div>
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
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Product Type *</label>
            <select v-model="productForm.product_type" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm">
              <option value="storable">Storable Product</option>
              <option value="consumable">Consumable</option>
              <option value="service">Service</option>
              <option value="digital">Digital Product</option>
            </select>
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Valuation Method</label>
            <select v-model="productForm.valuation_method" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm"
              :disabled="['service','digital'].includes(productForm.product_type)">
              <option value="average">Weighted Average</option>
              <option value="fifo">FIFO</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Barcode</label>
            <input v-model="productForm.barcode" placeholder="Optional" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
          <div v-if="productForm.product_type === 'digital'">
            <label class="text-xs text-gray-500 mb-1 block">Digital URL</label>
            <input v-model="productForm.digital_url" placeholder="https://..." style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
        </div>
        <div class="flex gap-6 pt-1">
          <label class="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
            <input type="checkbox" v-model="productForm.can_be_purchased" class="rounded" />
            Can be Purchased
          </label>
          <label class="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
            <input type="checkbox" v-model="productForm.can_be_sold" class="rounded" />
            Can be Sold
          </label>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Reorder Point</label>
            <input v-model="productForm.reorder_point" type="number" step="0.01" placeholder="0"
              style="color:#111827" class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Reorder Qty</label>
            <input v-model="productForm.reorder_qty" type="number" step="0.01" placeholder="0"
              style="color:#111827" class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
        </div>
        <p v-if="productModal.error" class="text-xs text-red-500">{{ productModal.error }}</p>
        <div class="flex justify-end gap-3 pt-1">
          <button @click="productModal.open = false" class="text-sm text-gray-500 px-4 py-2">Cancel</button>
          <button @click="saveProduct"
            class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
            {{ productModal.editing ? 'Save' : 'Create' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ── CATEGORY MODAL ── -->
    <div v-if="categoryModal.open" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 space-y-3">
        <h3 class="text-base font-semibold text-gray-800">{{ categoryModal.editing ? 'Edit Category' : 'New Category' }}</h3>
        <div>
          <label class="text-xs text-gray-500 mb-1 block">Name *</label>
          <input v-model="categoryForm.name" placeholder="Category name" style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        </div>
        <div>
          <label class="text-xs text-gray-500 mb-1 block">Parent Category</label>
          <select v-model="categoryForm.parent" style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm">
            <option :value="null">None</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
        <p v-if="categoryModal.error" class="text-xs text-red-500">{{ categoryModal.error }}</p>
        <div class="flex justify-end gap-3 pt-1">
          <button @click="categoryModal.open = false" class="text-sm text-gray-500 px-4 py-2">Cancel</button>
          <button @click="saveCategory"
            class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
            {{ categoryModal.editing ? 'Save' : 'Create' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ── UOM MODAL ── -->
    <div v-if="uomModal.open" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 space-y-3">
        <h3 class="text-base font-semibold text-gray-800">{{ uomModal.editing ? 'Edit UOM' : 'New UOM' }}</h3>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Name *</label>
            <input v-model="uomForm.name" placeholder="e.g. Kilogram" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Symbol *</label>
            <input v-model="uomForm.symbol" placeholder="e.g. kg" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
        </div>
        <div>
          <label class="text-xs text-gray-500 mb-1 block">Category *</label>
          <select v-model="uomForm.category" style="color:#111827"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm">
            <option value="">Select</option>
            <option value="unit">Unit</option>
            <option value="weight">Weight</option>
            <option value="volume">Volume</option>
            <option value="length">Length</option>
            <option value="time">Time</option>
            <option value="other">Other</option>
          </select>
        </div>
        <p v-if="uomModal.error" class="text-xs text-red-500">{{ uomModal.error }}</p>
        <div class="flex justify-end gap-3 pt-1">
          <button @click="uomModal.open = false" class="text-sm text-gray-500 px-4 py-2">Cancel</button>
          <button @click="saveUom"
            class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
            {{ uomModal.editing ? 'Save' : 'Create' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import client from '../api/client'

const activeTab = ref('Products')
const tabs      = ['Products', 'Categories', 'UOMs', 'Stock', 'Alerts']

const products   = ref([])
const categories = ref([])
const uoms       = ref([])
const quants     = ref([])
const alerts     = ref([])

// Modals
const productModal  = ref({ open: false, editing: false, id: null, error: '' })
const productForm   = ref({})
const categoryModal = ref({ open: false, editing: false, id: null, error: '' })
const categoryForm  = ref({})
const uomModal      = ref({ open: false, editing: false, id: null, error: '' })
const uomForm       = ref({})

// Helpers
function fmt(val) {
  return Number(val || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
function typeClass(type) {
  const map = {
    storable:   'bg-blue-100 text-blue-700',
    consumable: 'bg-yellow-100 text-yellow-700',
    service:    'bg-purple-100 text-purple-700',
    digital:    'bg-green-100 text-green-700',
  }
  return map[type] || 'bg-gray-100 text-gray-600'
}
function categoryName(id) {
  return categories.value.find(c => c.id === id)?.name || null
}
function uomSymbol(id) {
  const u = uoms.value.find(u => u.id === id)
  return u ? `${u.name} (${u.symbol})` : '—'
}

// Product CRUD
function openProductModal(p = null) {
  productModal.value = { open: true, editing: !!p, id: p?.id, error: '' }
  productForm.value  = p
    ? { ...p }
    : { name: '', sku: '', barcode: '', category: '', uom: '', cost: '', sales_price: '', valuation_method: 'average', reorder_point: 0, reorder_qty: 0, product_type: 'storable', can_be_purchased: true, can_be_sold: true, digital_url: '' }
}
async function saveProduct() {
  productModal.value.error = ''
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

// Category CRUD
function openCategoryModal(c = null) {
  categoryModal.value = { open: true, editing: !!c, id: c?.id, error: '' }
  categoryForm.value  = c ? { ...c } : { name: '', parent: null }
}
async function saveCategory() {
  categoryModal.value.error = ''
  try {
    if (categoryModal.value.editing) {
      await client.patch(`/inventory/categories/${categoryModal.value.id}/`, categoryForm.value)
    } else {
      await client.post('/inventory/categories/', categoryForm.value)
    }
    categoryModal.value.open = false
    loadCategories()
  } catch (e) {
    categoryModal.value.error = JSON.stringify(e.response?.data || 'Error')
  }
}
async function deleteCategory(id) {
  if (!confirm('Delete this category?')) return
  try { await client.delete(`/inventory/categories/${id}/`); loadCategories() } catch {}
}

// UOM CRUD
function openUomModal(u = null) {
  uomModal.value = { open: true, editing: !!u, id: u?.id, error: '' }
  uomForm.value  = u ? { ...u } : { name: '', symbol: '', category: '' }
}
async function saveUom() {
  uomModal.value.error = ''
  try {
    if (uomModal.value.editing) {
      await client.patch(`/inventory/uom/${uomModal.value.id}/`, uomForm.value)
    } else {
      await client.post('/inventory/uom/', uomForm.value)
    }
    uomModal.value.open = false
    loadUoms()
  } catch (e) {
    uomModal.value.error = JSON.stringify(e.response?.data || 'Error')
  }
}
async function deleteUom(id) {
  if (!confirm('Delete this UOM?')) return
  try { await client.delete(`/inventory/uom/${id}/`); loadUoms() } catch {}
}

// Loaders
async function loadProducts() {
  try { const r = await client.get('/inventory/products/'); products.value = r.data.results || r.data } catch {}
}
async function loadCategories() {
  try { const r = await client.get('/inventory/categories/'); categories.value = r.data.results || r.data } catch {}
}
async function loadUoms() {
  try { const r = await client.get('/inventory/uom/'); uoms.value = r.data.results || r.data } catch {}
}

onMounted(async () => {
  loadProducts()
  loadCategories()
  loadUoms()
  try { const r = await client.get('/inventory/stock-quants/'); quants.value = r.data.results || r.data } catch {}
  try { const r = await client.get('/inventory/low-stock/'); alerts.value = r.data.results || r.data } catch {}
})
</script>
