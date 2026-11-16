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
// //// Neoffice — the entries a sales representative does not have (see `utils/navigation.js`)
import { HIDDEN_FOR_REPRESENTATIVES } from '@/utils/navigation'
import { usersStore } from '@/stores/users'
// //// Neoffice — the pages that apps add to the menu (`crm.api.extension_tabs.get_pages`), in a group after the CRM's own entries
import { extensionPagesStore } from '@/stores/extensionPages'

import { useRouter, useRoute } from 'vue-router'
import { ref, computed } from 'vue'

const router = useRouter()
const { isRepresentative } = usersStore()
const extensionPages = extensionPagesStore()
const route = useRoute()
const failed = ref(false)

const surfaceApp = {
  name: 'crm',
  title: 'CRM',
  logo: '/assets/crm/images/logo.svg',
}

// fixed links carry icon COMPONENTS in AppSidebar — lucide strings here.
//// Neoffice — `detail` added: the router name of the single-record route that
//// belongs to a list entry, so that opening one record keeps its list
//// highlighted. Only the four entries that have such a route in router.js
//// carry it; Dashboard, Notes, Tasks and Call Logs have no detail route.
//// Neoffice — each label is a literal __() call made when the menu is drawn: the
//// cockpit showed these entries in English (« Leads », « Deals », « Call Logs »…)
//// under a French page, and a literal is what the catalogue extraction finds (07.10).
const LINKS = [
  {
    label: () => __('Dashboard'),
    icon: 'lucide-layout-dashboard',
    to: 'Dashboard',
  },
  {
    label: () => __('Leads'),
    icon: 'lucide-target',
    to: 'Leads',
    detail: 'Lead',
  },
  {
    label: () => __('Deals'),
    icon: 'lucide-hand-coins',
    to: 'Deals',
    detail: 'Deal',
  },
  {
    label: () => __('Contacts'),
    icon: 'lucide-contact',
    to: 'Contacts',
    detail: 'Contact',
  },
  {
    label: () => __('Organizations'),
    icon: 'lucide-building',
    to: 'Organizations',
    detail: 'Organization',
  },
  { label: () => __('Notes'), icon: 'lucide-sticky-note', to: 'Notes' },
  { label: () => __('Tasks'), icon: 'lucide-check-square', to: 'Tasks' },
  { label: () => __('Call Logs'), icon: 'lucide-phone', to: 'Call Logs' },
]

function navigate(r) {
  if (!r) return
  if (r.startsWith('/app') || r.startsWith('http')) window.location.href = r
  else router.push(r)
}

const contextNav = computed(() => {
  const currentName = route.name
  //// Neoffice — a sales representative's menu leaves out what is not theirs (deals, contacts, organizations)
  const links = isRepresentative()
    ? LINKS.filter((item) => !HIDDEN_FOR_REPRESENTATIVES.includes(item.to))
    : LINKS
  //// Neoffice — the pages an app adds (the hub's funnel and cards, for its managers), each lit on its own route
  const pages = (extensionPages.pages.data || []).map((page) => ({
    label: page.label,
    icon: page.icon || 'lucide-layout-panel-left',
    active: currentName === 'TeamPage' && route.params.name === page.name,
    onClick: () =>
      router.push({ name: 'TeamPage', params: { name: page.name } }),
  }))
  return [
    {
      items: links.map((item) => ({
        //// Neoffice — translated here, see LINKS.
        label: item.label(),
        icon: item.icon,
        //// Neoffice — match the router name exactly, on the list route or on
        //// the detail route this entry owns. The previous test was
        //// String(currentName).startsWith(item.to) — the wrong way round: the
        //// detail names are shorter than the list names ('Lead'.startsWith(
        //// 'Leads') is false), so opening a record un-highlighted the whole
        //// sidebar instead of keeping its list lit. The currentName guard
        //// keeps an unnamed route (initial navigation) from lighting every
        //// entry whose `detail` is undefined.
        active:
          //// Neoffice — see the note just above.
          !!currentName &&
          (currentName === item.to || currentName === item.detail),
        onClick: () => router.push({ name: item.to }),
      })),
    },
    //// Neoffice — a group of their own, only when an app adds a page
    ...(pages.length ? [{ items: pages }] : []),
  ]
})
</script>
