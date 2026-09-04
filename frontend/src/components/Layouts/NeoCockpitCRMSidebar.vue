<!-- //// Neoffice — added file (no upstream equivalent): the CRM flavour of the
//// shared Neoffice chrome (NeoCockpit). DesktopLayout mounts it in place of
//// upstream's AppSidebar; it maps CRM's fixed links into contextNav and falls
//// back to AppSidebar on its own when the cockpit bundle cannot load.
//// Commit b4be8086. -->
<template>
  <AppSidebar v-if="failed" />
  <NeoCockpitBridge
    v-else
    :surface-app="surfaceApp"
    :context-nav="contextNav"
    :navigate="navigate"
    @failed="failed = true"
  />
</template>

<script setup>
/**
 * CRM flavor of the shared Neoffice chrome (NeoCockpit). Maps the fixed
 * links (Dashboard/Leads/Deals/…) into contextNav; the native AppSidebar
 * stays as an automatic fallback. No onSearch: CRM has no global command
 * palette today (custom views keep working through the native fallback).
 * Recipe: neoffice ADR-015.
 */
import AppSidebar from '@/components/Layouts/AppSidebar.vue'
import NeoCockpitBridge from '@/components/NeoCockpitBridge.vue'

import { useRouter, useRoute } from 'vue-router'
import { ref, computed } from 'vue'

const router = useRouter()
const route = useRoute()
const failed = ref(false)

const surfaceApp = {
  name: 'crm',
  title: 'CRM',
  logo: '/assets/crm/images/logo.svg',
}

// fixed links carry icon COMPONENTS in AppSidebar — lucide strings here
const LINKS = [
  { label: 'Dashboard', icon: 'lucide-layout-dashboard', to: 'Dashboard' },
  { label: 'Leads', icon: 'lucide-target', to: 'Leads' },
  { label: 'Deals', icon: 'lucide-hand-coins', to: 'Deals' },
  { label: 'Contacts', icon: 'lucide-contact', to: 'Contacts' },
  { label: 'Organizations', icon: 'lucide-building', to: 'Organizations' },
  { label: 'Notes', icon: 'lucide-sticky-note', to: 'Notes' },
  { label: 'Tasks', icon: 'lucide-check-square', to: 'Tasks' },
  { label: 'Call Logs', icon: 'lucide-phone', to: 'Call Logs' },
]

function navigate(r) {
  if (!r) return
  if (r.startsWith('/app') || r.startsWith('http')) window.location.href = r
  else router.push(r)
}

const contextNav = computed(() => {
  const currentName = route.name
  return [
    {
      items: LINKS.map((item) => ({
        label: item.label,
        icon: item.icon,
        active:
          currentName === item.to ||
          String(currentName || '').startsWith(item.to.replace(/ /g, '')),
        onClick: () => router.push({ name: item.to }),
      })),
    },
  ]
})
</script>
