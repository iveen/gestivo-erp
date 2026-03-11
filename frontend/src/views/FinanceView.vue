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
        <button @click="openAccountModal()"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
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
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="accounts.length === 0">
              <td colspan="5" class="px-4 py-6 text-center text-gray-400">No accounts found</td>
            </tr>
            <tr v-for="account in accounts" :key="account.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 font-mono text-gray-600">{{ account.code }}</td>
              <td class="px-4 py-3 text-gray-800">{{ account.name }}</td>
              <td class="px-4 py-3 text-gray-500 capitalize">{{ account.account_type }}</td>
              <td class="px-4 py-3 text-gray-500 capitalize">{{ account.normal_balance }}</td>
              <td class="px-4 py-3 space-x-3">
                <button @click="openAccountModal(account)"
                  class="text-xs text-blue-600 hover:underline">Edit</button>
                <button @click="deleteAccount(account.id)"
                  class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Journal Entries -->
    <div v-if="activeTab === 'Journal Entries'">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-semibold text-gray-700">Journal Entries</h3>
        <button @click="openEntryForm()"
          class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
          + New Entry
        </button>
      </div>

      <!-- Entry Form -->
      <div v-if="showEntryForm"
        class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6 space-y-4">
        <h4 class="text-sm font-semibold text-gray-700">
          {{ editingEntry ? 'Edit Journal Entry' : 'New Journal Entry' }}
        </h4>

        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Journal</label>
            <select v-model="entryForm.journal" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm">
              <option value="">Select Journal</option>
              <option v-for="j in journals" :key="j.id" :value="j.id">{{ j.name }}</option>
            </select>
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Date</label>
            <input v-model="entryForm.date" type="date" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Reference</label>
            <input v-model="entryForm.reference" placeholder="e.g. INV-001" style="color:#111827"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
          </div>
        </div>

        <!-- Lines -->
        <div>
          <div class="flex justify-between items-center mb-2">
            <label class="text-xs text-gray-500">Entry Lines</label>
            <button @click="addLine()"
              class="text-xs text-blue-600 hover:underline">+ Add Line</button>
          </div>
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
              <tr>
                <th class="text-left px-3 py-2">Account</th>
                <th class="text-left px-3 py-2">Description</th>
                <th class="text-right px-3 py-2">Debit</th>
                <th class="text-right px-3 py-2">Credit</th>
                <th class="px-3 py-2"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(line, i) in entryForm.lines" :key="i"
                class="border-t border-gray-50">
                <td class="px-2 py-1">
                  <select v-model="line.account" style="color:#111827"
                    class="w-full border border-gray-200 rounded px-2 py-1 text-sm">
                    <option value="">Select Account</option>
                    <option v-for="a in accounts" :key="a.id" :value="a.id">
                      {{ a.code }} - {{ a.name }}
                    </option>
                  </select>
                </td>
                <td class="px-2 py-1">
                  <input v-model="line.description" placeholder="Description" style="color:#111827"
                    class="w-full border border-gray-200 rounded px-2 py-1 text-sm" />
                </td>
                <td class="px-2 py-1">
                  <input v-model="line.debit" type="number" step="0.01" placeholder="0.00"
                    style="color:#111827"
                    class="w-full border border-gray-200 rounded px-2 py-1 text-sm text-right"
                    @input="line.credit = line.debit > 0 ? '0.00' : line.credit" />
                </td>
                <td class="px-2 py-1">
                  <input v-model="line.credit" type="number" step="0.01" placeholder="0.00"
                    style="color:#111827"
                    class="w-full border border-gray-200 rounded px-2 py-1 text-sm text-right"
                    @input="line.debit = line.credit > 0 ? '0.00' : line.debit" />
                </td>
                <td class="px-2 py-1 text-center">
                  <button @click="removeLine(i)"
                    class="text-red-400 hover:text-red-600 text-xs">✕</button>
                </td>
              </tr>
            </tbody>
            <tfoot class="border-t border-gray-200">
              <tr>
                <td colspan="2" class="px-3 py-2 text-right text-xs text-gray-500">Totals</td>
                <td class="px-3 py-2 text-right text-sm font-semibold"
                  :class="isBalanced ? 'text-green-600' : 'text-red-500'">
                  {{ totalDebit.toFixed(2) }}
                </td>
                <td class="px-3 py-2 text-right text-sm font-semibold"
                  :class="isBalanced ? 'text-green-600' : 'text-red-500'">
                  {{ totalCredit.toFixed(2) }}
                </td>
                <td></td>
              </tr>
            </tfoot>
          </table>
          <p v-if="!isBalanced && entryForm.lines.length > 0"
            class="text-xs text-red-500 mt-1">
            ⚠ Entry is not balanced. Debits must equal credits.
          </p>
          <p v-if="isBalanced && entryForm.lines.length > 0"
            class="text-xs text-green-600 mt-1">
            ✓ Entry is balanced.
          </p>
        </div>

        <p v-if="entryError" class="text-xs text-red-500">{{ entryError }}</p>

        <div class="flex justify-end gap-3">
          <button @click="showEntryForm = false"
            class="text-sm text-gray-500 hover:text-gray-700 px-4 py-2">Cancel</button>
          <button @click="saveEntry(false)"
            class="border border-blue-800 text-blue-800 text-sm px-4 py-2 rounded-lg hover:bg-blue-50">
            Save as Draft
          </button>
          <button @click="saveEntry(true)" :disabled="!isBalanced"
            class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900 disabled:opacity-50">
            Save & Post
          </button>
        </div>
      </div>

      <!-- Entries List -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-4 py-3">Date</th>
              <th class="text-left px-4 py-3">Reference</th>
              <th class="text-left px-4 py-3">Journal</th>
              <th class="text-right px-4 py-3">Total Debit</th>
              <th class="text-left px-4 py-3">Status</th>
              <th class="text-left px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="entries.length === 0">
              <td colspan="6" class="px-4 py-6 text-center text-gray-400">No journal entries found</td>
            </tr>
            <tr v-for="entry in entries" :key="entry.id"
              class="border-t border-gray-50 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-600">{{ entry.date }}</td>
              <td class="px-4 py-3 text-gray-800">{{ entry.reference || '—' }}</td>
              <td class="px-4 py-3 text-gray-500">{{ journalName(entry.journal) }}</td>
              <td class="px-4 py-3 text-right text-gray-800 font-medium">
                {{ entryTotal(entry) }}
              </td>
              <td class="px-4 py-3">
                <span :class="entry.is_posted
                  ? 'bg-green-100 text-green-700'
                  : 'bg-yellow-100 text-yellow-700'"
                  class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ entry.is_posted ? 'Posted' : 'Draft' }}
                </span>
              </td>
              <td class="px-4 py-3 space-x-3">
                <button v-if="!entry.is_posted" @click="postEntry(entry.id)"
                  class="text-xs text-green-600 hover:underline">Post</button>
                <button @click="viewEntry(entry)"
                  class="text-xs text-blue-600 hover:underline">View</button>
                <button v-if="!entry.is_posted" @click="deleteEntry(entry.id)"
                  class="text-xs text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Entry Detail Modal -->
    <div v-if="selectedEntry"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-2xl p-6 space-y-4">
        <div class="flex justify-between items-center">
          <h3 class="text-base font-semibold text-gray-800">Journal Entry Detail</h3>
          <button @click="selectedEntry = null" class="text-gray-400 hover:text-gray-600">✕</button>
        </div>
        <div class="grid grid-cols-3 gap-4 text-sm">
          <div><span class="text-gray-400">Date</span><p class="font-medium">{{ selectedEntry.date }}</p></div>
          <div><span class="text-gray-400">Reference</span><p class="font-medium">{{ selectedEntry.reference || '—' }}</p></div>
          <div><span class="text-gray-400">Status</span>
            <span :class="selectedEntry.is_posted ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
              class="px-2 py-1 rounded-full text-xs font-medium">
              {{ selectedEntry.is_posted ? 'Posted' : 'Draft' }}
            </span>
          </div>
        </div>
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-400 text-xs uppercase">
            <tr>
              <th class="text-left px-3 py-2">Account</th>
              <th class="text-left px-3 py-2">Description</th>
              <th class="text-right px-3 py-2">Debit</th>
              <th class="text-right px-3 py-2">Credit</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="line in selectedEntry.lines" :key="line.id"
              class="border-t border-gray-50">
              <td class="px-3 py-2 text-gray-700">
                {{ line.account_code }} - {{ line.account_name }}
              </td>
              <td class="px-3 py-2 text-gray-500">{{ line.description || '—' }}</td>
              <td class="px-3 py-2 text-right text-gray-800">{{ line.debit }}</td>
              <td class="px-3 py-2 text-right text-gray-800">{{ line.credit }}</td>
            </tr>
          </tbody>
        </table>
        <div class="flex justify-end gap-3">
          <button v-if="!selectedEntry.is_posted" @click="postEntry(selectedEntry.id); selectedEntry = null"
            class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
            Post Entry
          </button>
          <button @click="selectedEntry = null"
            class="text-sm text-gray-500 hover:text-gray-700 px-4 py-2">Close</button>
        </div>
      </div>
    </div>

    <!-- Account Modal -->
    <div v-if="accountModal.open"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 space-y-4">
        <h3 class="text-base font-semibold text-gray-800">
          {{ accountModal.editing ? 'Edit Account' : 'New Account' }}
        </h3>
        <input v-model="accountForm.code" placeholder="Code (e.g. 1001)" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        <input v-model="accountForm.name" placeholder="Name" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        <select v-model="accountForm.account_type" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm">
          <option value="">Select Type</option>
          <option value="asset">Asset</option>
          <option value="liability">Liability</option>
          <option value="equity">Equity</option>
          <option value="revenue">Revenue</option>
          <option value="expense">Expense</option>
        </select>
        <input v-model="accountForm.currency" placeholder="Currency (e.g. USD)" style="color:#111827"
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
        <p v-if="accountModal.error" class="text-xs text-red-500">{{ accountModal.error }}</p>
        <div class="flex justify-end gap-3">
          <button @click="accountModal.open = false"
            class="text-sm text-gray-500 px-4 py-2">Cancel</button>
          <button @click="saveAccount"
            class="bg-blue-800 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-900">
            {{ accountModal.editing ? 'Save' : 'Create' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Reports -->
    <div v-if="activeTab === 'Reports'" class="space-y-6">
      <!-- Report Selector -->
      <div class="flex gap-3 items-center">
        <button v-for="r in reportTypes" :key="r"
          @click="activeReport = r"
          class="px-4 py-2 text-sm rounded-lg border transition"
          :class="activeReport === r
            ? 'bg-blue-800 text-white border-blue-800'
            : 'bg-white text-gray-600 border-gray-200 hover:border-blue-400'">
          {{ r }}
        </button>
      </div>

      <!-- Balance Sheet Controls -->
      <div v-if="activeReport === 'Balance Sheet'"
        class="bg-white rounded-xl shadow-sm border border-gray-100 p-5 space-y-4">
        <div class="flex justify-between items-center">
          <h3 class="text-sm font-semibold text-gray-700">Balance Sheet</h3>
          <div class="flex gap-3 items-center">
            <input v-model="bsDate" type="date" style="color:#111827"
              class="border border-gray-200 rounded-lg px-3 py-1.5 text-sm" />
            <button @click="loadBalanceSheet"
              class="bg-blue-800 text-white text-sm px-4 py-1.5 rounded-lg hover:bg-blue-900">
              Run Report
            </button>
          </div>
        </div>

        <div v-if="bsReport">
          <p class="text-xs text-gray-400 mb-4">As of {{ bsReport.as_of_date }} · {{ bsReport.currency }}</p>

          <!-- Assets -->
          <div class="mb-4">
            <div class="flex justify-between items-center bg-gray-50 px-4 py-2 rounded-lg mb-1">
              <span class="text-xs font-semibold text-gray-600 uppercase">Assets</span>
              <span class="text-sm font-semibold text-gray-800">{{ fmt(bsReport.assets.total) }}</span>
            </div>
            <table class="w-full text-sm">
              <tbody>
                <tr v-for="item in bsReport.assets.items" :key="item.code"
                  class="border-t border-gray-50">
                  <td class="px-4 py-2 font-mono text-gray-500 text-xs">{{ item.code }}</td>
                  <td class="px-4 py-2 text-gray-700">{{ item.name }}</td>
                  <td class="px-4 py-2 text-right"
                    :class="item.balance < 0 ? 'text-red-500' : 'text-gray-800'">
                    {{ fmt(item.balance) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Liabilities -->
          <div class="mb-4">
            <div class="flex justify-between items-center bg-gray-50 px-4 py-2 rounded-lg mb-1">
              <span class="text-xs font-semibold text-gray-600 uppercase">Liabilities</span>
              <span class="text-sm font-semibold text-gray-800">{{ fmt(bsReport.liabilities.total) }}</span>
            </div>
            <table class="w-full text-sm">
              <tbody>
                <tr v-for="item in bsReport.liabilities.items" :key="item.code"
                  class="border-t border-gray-50">
                  <td class="px-4 py-2 font-mono text-gray-500 text-xs">{{ item.code }}</td>
                  <td class="px-4 py-2 text-gray-700">{{ item.name }}</td>
                  <td class="px-4 py-2 text-right text-gray-800">{{ fmt(item.balance) }}</td>
                </tr>
                <tr v-if="bsReport.liabilities.items.length === 0">
                  <td colspan="3" class="px-4 py-2 text-gray-400 text-xs">No liabilities</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Equity -->
          <div class="mb-4">
            <div class="flex justify-between items-center bg-gray-50 px-4 py-2 rounded-lg mb-1">
              <span class="text-xs font-semibold text-gray-600 uppercase">Equity</span>
              <span class="text-sm font-semibold text-gray-800">{{ fmt(bsReport.equity.total) }}</span>
            </div>
            <table class="w-full text-sm">
              <tbody>
                <tr v-for="item in bsReport.equity.items" :key="item.code"
                  class="border-t border-gray-50">
                  <td class="px-4 py-2 font-mono text-gray-500 text-xs">{{ item.code }}</td>
                  <td class="px-4 py-2 text-gray-700">{{ item.name }}</td>
                  <td class="px-4 py-2 text-right text-gray-800">{{ fmt(item.balance) }}</td>
                </tr>
                <tr v-if="bsReport.equity.items.length === 0">
                  <td colspan="3" class="px-4 py-2 text-gray-400 text-xs">No equity accounts</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Total -->
          <div class="border-t-2 border-gray-200 pt-3 flex justify-between items-center px-4">
            <span class="text-sm font-semibold text-gray-700">Total Liabilities + Equity</span>
            <span class="text-sm font-semibold"
              :class="bsReport.is_balanced ? 'text-green-600' : 'text-red-500'">
              {{ fmt(bsReport.liabilities.total + bsReport.equity.total) }}
              <span v-if="!bsReport.is_balanced" class="text-xs ml-1">(unbalanced)</span>
            </span>
          </div>
        </div>
        <p v-else class="text-xs text-gray-400">Select a date and click Run Report.</p>
      </div>

      <!-- P&L Controls -->
      <div v-if="activeReport === 'Profit & Loss'"
        class="bg-white rounded-xl shadow-sm border border-gray-100 p-5 space-y-4">
        <div class="flex justify-between items-center">
          <h3 class="text-sm font-semibold text-gray-700">Profit & Loss</h3>
          <div class="flex gap-3 items-center">
            <input v-model="plStart" type="date" style="color:#111827"
              class="border border-gray-200 rounded-lg px-3 py-1.5 text-sm" />
            <span class="text-xs text-gray-400">to</span>
            <input v-model="plEnd" type="date" style="color:#111827"
              class="border border-gray-200 rounded-lg px-3 py-1.5 text-sm" />
            <button @click="loadPL"
              class="bg-blue-800 text-white text-sm px-4 py-1.5 rounded-lg hover:bg-blue-900">
              Run Report
            </button>
          </div>
        </div>

        <div v-if="plReport">
          <p class="text-xs text-gray-400 mb-4">
            {{ plReport.period.start }} to {{ plReport.period.end }} · {{ plReport.currency }}
          </p>

          <!-- Revenue -->
          <div class="mb-4">
            <div class="flex justify-between items-center bg-gray-50 px-4 py-2 rounded-lg mb-1">
              <span class="text-xs font-semibold text-gray-600 uppercase">Revenue</span>
              <span class="text-sm font-semibold text-green-600">{{ fmt(plReport.revenue.total) }}</span>
            </div>
            <table class="w-full text-sm">
              <tbody>
                <tr v-for="item in plReport.revenue.items" :key="item.code"
                  class="border-t border-gray-50">
                  <td class="px-4 py-2 font-mono text-gray-500 text-xs">{{ item.code }}</td>
                  <td class="px-4 py-2 text-gray-700">{{ item.name }}</td>
                  <td class="px-4 py-2 text-right text-green-600">{{ fmt(item.balance) }}</td>
                </tr>
                <tr v-if="plReport.revenue.items.length === 0">
                  <td colspan="3" class="px-4 py-2 text-gray-400 text-xs">No revenue</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Expenses -->
          <div class="mb-4">
            <div class="flex justify-between items-center bg-gray-50 px-4 py-2 rounded-lg mb-1">
              <span class="text-xs font-semibold text-gray-600 uppercase">Expenses</span>
              <span class="text-sm font-semibold text-red-500">{{ fmt(plReport.expenses.total) }}</span>
            </div>
            <table class="w-full text-sm">
              <tbody>
                <tr v-for="item in plReport.expenses.items" :key="item.code"
                  class="border-t border-gray-50">
                  <td class="px-4 py-2 font-mono text-gray-500 text-xs">{{ item.code }}</td>
                  <td class="px-4 py-2 text-gray-700">{{ item.name }}</td>
                  <td class="px-4 py-2 text-right text-red-500">{{ fmt(item.balance) }}</td>
                </tr>
                <tr v-if="plReport.expenses.items.length === 0">
                  <td colspan="3" class="px-4 py-2 text-gray-400 text-xs">No expenses</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Net Income -->
          <div class="border-t-2 border-gray-200 pt-3 flex justify-between items-center px-4">
            <span class="text-sm font-semibold text-gray-700">Net Income</span>
            <span class="text-base font-bold"
              :class="plReport.net_income >= 0 ? 'text-green-600' : 'text-red-500'">
              {{ fmt(plReport.net_income) }}
            </span>
          </div>
        </div>
        <p v-else class="text-xs text-gray-400">Select a date range and click Run Report.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import client from '../api/client'

const activeTab = ref('Chart of Accounts')
const tabs      = ['Chart of Accounts', 'Journal Entries', 'Reports']
const accounts  = ref([])
const journals  = ref([])
const entries   = ref([])

// Entry form
const showEntryForm = ref(false)
const editingEntry  = ref(null)
const entryError    = ref('')
const selectedEntry = ref(null)
const entryForm     = ref({ journal: '', date: '', reference: '', lines: [] })

// Reports
const reportTypes  = ['Balance Sheet', 'Profit & Loss']
const activeReport = ref('Balance Sheet')
const bsDate  = ref(new Date().toISOString().slice(0, 10))
const plStart = ref(new Date(new Date().getFullYear(), 0, 1).toISOString().slice(0, 10))
const plEnd   = ref(new Date().toISOString().slice(0, 10))
const bsReport = ref(null)
const plReport = ref(null)

async function loadBalanceSheet() {
  try {
    const res = await client.get(`/finance/reports/balance_sheet/?as_of=${bsDate.value}`)
    bsReport.value = res.data
  } catch {}
}

async function loadPL() {
  try {
    const res = await client.get(`/finance/reports/profit_loss/?start=${plStart.value}&end=${plEnd.value}`)
    plReport.value = res.data
  } catch {}
}

function fmt(val) {
  if (val === null || val === undefined) return '0.00'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

// Account modal
const accountModal = ref({ open: false, editing: false, id: null, error: '' })
const accountForm  = ref({})

function openEntryForm() {
  editingEntry.value  = null
  entryError.value    = ''
  entryForm.value     = {
    journal: journals.value[0]?.id || '',
    date: new Date().toISOString().slice(0, 10),
    reference: '',
    lines: [
      { account: '', description: '', debit: '', credit: '' },
      { account: '', description: '', debit: '', credit: '' },
    ]
  }
  showEntryForm.value = true
}

function addLine() {
  entryForm.value.lines.push({ account: '', description: '', debit: '', credit: '' })
}

function removeLine(i) {
  entryForm.value.lines.splice(i, 1)
}

const totalDebit  = computed(() =>
  entryForm.value.lines.reduce((s, l) => s + (parseFloat(l.debit) || 0), 0)
)
const totalCredit = computed(() =>
  entryForm.value.lines.reduce((s, l) => s + (parseFloat(l.credit) || 0), 0)
)
const isBalanced  = computed(() =>
  entryForm.value.lines.length > 0 &&
  Math.abs(totalDebit.value - totalCredit.value) < 0.001 &&
  totalDebit.value > 0
)

function entryTotal(entry) {
  if (!entry.lines) return '—'
  const total = entry.lines.reduce((s, l) => s + parseFloat(l.debit || 0), 0)
  return total.toFixed(2)
}

async function saveEntry(postImmediately) {
  entryError.value = ''
  if (!entryForm.value.journal) { entryError.value = 'Select a journal'; return }
  if (!entryForm.value.date)    { entryError.value = 'Select a date'; return }
  if (entryForm.value.lines.length < 2) { entryError.value = 'Add at least 2 lines'; return }

  const payload = {
    journal:   entryForm.value.journal,
    date:      entryForm.value.date,
    reference: entryForm.value.reference,
    is_posted: false,
    lines: entryForm.value.lines.map(l => ({
      account:     l.account,
      description: l.description,
      debit:       parseFloat(l.debit)  || 0,
      credit:      parseFloat(l.credit) || 0,
    }))
  }

  try {
    const res = await client.post('/finance/journal-entries/', payload)
    if (postImmediately && isBalanced.value) {
      await client.post(`/finance/journal-entries/${res.data.id}/post_entry/`)
    }
    showEntryForm.value = false
    loadEntries()
  } catch (e) {
    entryError.value = JSON.stringify(e.response?.data || 'Error saving entry')
  }
}

async function postEntry(id) {
  try {
    await client.post(`/finance/journal-entries/${id}/post_entry/`)
    loadEntries()
  } catch {}
}

async function deleteEntry(id) {
  if (!confirm('Delete this draft entry?')) return
  try {
    await client.delete(`/finance/journal-entries/${id}/`)
    loadEntries()
  } catch {}
}

function journalName(id) {
  const j = journals.value.find(j => j.id === id)
  return j ? j.name : id
}

function viewEntry(entry) {
  selectedEntry.value = entry
}

function openAccountModal(account = null) {
  accountModal.value = { open: true, editing: !!account, id: account?.id, error: '' }
  accountForm.value  = account
    ? { ...account }
    : { code: '', name: '', account_type: '', currency: 'USD' }
}

async function saveAccount() {
  try {
    if (accountModal.value.editing) {
      await client.patch(`/finance/accounts/${accountModal.value.id}/`, accountForm.value)
    } else {
      await client.post('/finance/accounts/', accountForm.value)
    }
    accountModal.value.open = false
    loadAccounts()
  } catch (e) {
    accountModal.value.error = JSON.stringify(e.response?.data || 'Error saving')
  }
}

async function deleteAccount(id) {
  if (!confirm('Delete this account?')) return
  try {
    await client.delete(`/finance/accounts/${id}/`)
    loadAccounts()
  } catch {}
}

async function loadAccounts() {
  try {
    const res = await client.get('/finance/accounts/')
    accounts.value = res.data.results || res.data
  } catch {}
}

async function loadEntries() {
  try {
    const res = await client.get('/finance/journal-entries/')
    entries.value = res.data.results || res.data
  } catch {}
}

onMounted(async () => {
  loadAccounts()
  loadEntries()
  try {
    const res = await client.get('/finance/journals/')
    journals.value = res.data.results || res.data
  } catch {}
})
</script>