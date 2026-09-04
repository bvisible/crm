<template>
  <div class="flex h-screen w-screen">
    <div class="h-full border-r bg-surface-menu-bar">
      <!-- //// Neoffice — upstream mounts <AppSidebar /> here. We mount the shared
      //// Neoffice chrome (NeoCockpit) instead, so CRM carries the same sidebar as
      //// the desk and the other SPAs; NeoCockpitCRMSidebar keeps AppSidebar as its
      //// automatic fallback when the cockpit bundle fails. Commit b4be8086. -->
      <NeoCockpitCRMSidebar />
    </div>
    <div class="flex-1 flex flex-col h-full overflow-auto bg-surface-white">
      <AppHeader />
      <slot />
    </div>
    <GlobalModals />
  </div>
</template>
<script setup>
//// Neoffice — was: import AppSidebar from '@/components/Layouts/AppSidebar.vue'.
//// The wrapper still imports AppSidebar itself, so upstream's component stays
//// reachable as the fallback. Commit b4be8086.
import NeoCockpitCRMSidebar from '@/components/Layouts/NeoCockpitCRMSidebar.vue'
import AppHeader from '@/components/Layouts/AppHeader.vue'
import GlobalModals from '@/components/Modals/GlobalModals.vue'
</script>
