<!-- //// Neoffice — added file (no upstream equivalent) -->
<!-- //// A page that an app adds to the CRM's menu (`crm.api.extension_tabs.get_pages`): the funnel and the cards of the hub's
     representatives. The app's page is shown in a frame, like a tab of a lead's page (`ExtensionTab.vue`); no code of the app
     lives in this public fork, and an account the app does not give the page to is told it is not permitted. -->
<template>
  <LayoutHeader>
    <template #left-header>
      <Breadcrumbs :items="breadcrumbs" />
    </template>
  </LayoutHeader>
  <div v-if="page" class="flex min-h-0 flex-1 flex-col">
    <ExtensionTab :tab="page" docname="" />
  </div>
  <div
    v-else-if="!pages.loading"
    class="flex flex-1 items-center justify-center text-p-base text-ink-gray-5"
  >
    {{ __('Not permitted') }}
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import ExtensionTab from '@/components/ExtensionTab.vue'
import { Breadcrumbs } from 'frappe-ui'
import { extensionPagesStore } from '@/stores/extensionPages'
import { computed } from 'vue'

const props = defineProps({
  name: { type: String, required: true },
})

const store = extensionPagesStore()
const { pages } = store
const page = computed(() => store.getPage(props.name))

const breadcrumbs = computed(() => [
  {
    label: page.value?.label || '',
    route: { name: 'TeamPage', params: { name: props.name } },
  },
])
</script>
