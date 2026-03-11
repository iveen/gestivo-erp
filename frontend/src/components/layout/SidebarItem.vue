<template>
  <router-link
    :to="to"
    class="flex items-center px-3 py-2 rounded-lg text-sm transition"
    :class="isActive
      ? 'bg-blue-700 text-white'
      : 'text-blue-200 hover:bg-blue-800 hover:text-white'"
  >
    <span class="mr-3">
      <component :is="iconComponent" class="w-5 h-5" />
    </span>
    {{ label }}
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  HomeIcon,
  CurrencyDollarIcon,
  CubeIcon,
  ShoppingCartIcon,
  TruckIcon,
  CogIcon,
  UsersIcon,
  WrenchScrewdriverIcon,
} from '@heroicons/vue/24/outline'

const props = defineProps({
  to:    String,
  icon:  String,
  label: String,
})

const route    = useRoute()
const isActive = computed(() => route.path === props.to)

const icons = {
  'home':          HomeIcon,
  'currency':      CurrencyDollarIcon,
  'cube':          CubeIcon,
  'shopping-cart': ShoppingCartIcon,
  'truck':         TruckIcon,
  'cog':           CogIcon,
  'users':         UsersIcon,
  'wrench':        WrenchScrewdriverIcon,
}

const iconComponent = computed(() => icons[props.icon] || HomeIcon)
</script>