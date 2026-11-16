<!-- //// Neoffice — added file (no upstream equivalent) -->
<!-- //// A tab that another app adds to the page of a CRM document (the hub's representatives: their prospect's questions, offer,
     visits and presentation). The app says where its content is (a path of this site, `crm.api.extension_tabs.get_tabs`); the tab
     shows it in a frame of its own, so that no code of the app lives in this public fork, and passes the theme of the CRM. -->
<!-- //// Neoffice — the frame loads at once: a tab (or a page) is opened to be read, and the browser's lazy loading left a frame blank
     until something moved (seen on the hub, 16.11). -->
<template>
  <div class="flex h-full min-h-0 w-full flex-1 flex-col">
    <iframe
      :key="src"
      :src="src"
      :title="tab.label"
      class="h-full min-h-[480px] w-full flex-1 border-0"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  tab: { type: Object, required: true },
  docname: { type: String, required: true },
})

// The CRM draws itself dark or light by the `data-theme` of the page, else by the system's choice: the frame is told which.
function theme() {
  const set = document.documentElement.getAttribute('data-theme')
  if (set === 'dark' || set === 'light') return set
  return window.matchMedia?.('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light'
}

const src = computed(() => {
  // Only a path of this site, whatever an app wrote: a frame never opens another address.
  const path = String(props.tab.url || '').replace(
    '{docname}',
    encodeURIComponent(props.docname),
  )
  if (!path.startsWith('/') || path.startsWith('//')) return 'about:blank'
  const url = new URL(path, window.location.origin)
  url.searchParams.set('theme', theme())
  return url.pathname + url.search + url.hash
})
</script>
