<!-- //// Neoffice — added file (no upstream equivalent): mounts the shared
//// Neoffice chrome bundle (React IIFE, React inlined — no dependency added to
//// this Vue app) in place of the native frappe-ui Sidebar. Same recipe as the
//// Drive / LMS / Helpdesk bridges; it emits 'failed' so the host keeps the
//// native sidebar rather than losing its chrome. Commit b4be8086. -->
<template>
  <div
    ref="host"
    class="neocockpit-host hidden sm:block h-full flex-shrink-0"
  />
</template>

<script setup>
/**
 * NeoCockpitBridge — mounts the shared Neoffice chrome (React IIFE bundle,
 * React inlined — no dependency added to this Vue app) in place of the
 * native frappe-ui Sidebar.
 *
 * Generic recipe for every standalone Vue surface (Drive / LMS / Helpdesk /
 * CRM): copy this file, adapt the `contextNav` mapping to the app's own
 * sidebar items, pass the app identity via `surfaceApp`. Everything else
 * (module switcher, NORA, synk, mail, notifications, help, responsive
 * ladder) comes from the component for free.
 *
 * Boot: fetched once from neoffice_theme.cockpit_boot.get_cockpit_boot —
 * no www controller change in the host app.
 */
import { ref, onMounted, onUnmounted, watch } from "vue"

const props = defineProps({
  /** {name, title, logo} — how this app appears in the module switcher */
  surfaceApp: { type: Object, required: true },
  /** [{label?, items: [{label, icon, route|onClick, active, badge}]}] */
  contextNav: { type: Array, default: () => [] },
  /** {label, sub, percent, onClick} — e.g. Drive storage */
  contextFooter: { type: Object, default: null },
  /** SPA-internal navigation (vue-router push). /app/* falls back to a
   *  full page load automatically. */
  navigate: { type: Function, required: true },
  /** Open the app's own search overlay from the cockpit search bar. */
  onSearch: { type: Function, default: null },
  /** Keyboard hint shown in the search bar (the app's native shortcut). */
  searchKbd: { type: String, default: "" },
})

const host = ref(null)
const BUNDLE = "/assets/frappe/js/lib/neocockpit.global.js"
let mounted = false

function bundleUrl() {
  // cache-bust with the server build version (the asset has no hash of its own)
  const v = window.frappe?.boot?.cockpit_bundle_version || window.frappe?.boot?.assets_version || "1"
  return `${BUNDLE}?v=${encodeURIComponent(v)}`
}

function loadBundle() {
  return new Promise((resolve, reject) => {
    if (window.NeoCockpit && window.NeoCockpit.mount) return resolve()
    const existing = document.querySelector(`script[src^="${BUNDLE}"]`)
    if (existing) {
      existing.addEventListener("load", () => resolve())
      existing.addEventListener("error", reject)
      return
    }
    const s = document.createElement("script")
    s.src = bundleUrl()
    s.onload = () => resolve()
    s.onerror = () => reject(new Error("neocockpit bundle failed to load"))
    document.head.appendChild(s)
  })
}

async function loadBoot() {
  if (window.frappe?.boot?.app_data) return
  const r = await fetch(
    "/api/method/neoffice_theme.cockpit_boot.get_cockpit_boot",
    { credentials: "include", headers: { "X-Frappe-Site-Name": window.location.hostname } }
  )
  if (!r.ok) throw new Error("cockpit boot fetch failed: " + r.status)
  const boot = (await r.json()).message || {}
  window.frappe = window.frappe || {}
  window.frappe.boot = { ...(window.frappe.boot || {}), ...boot }
}

function render() {
  if (!host.value || !window.NeoCockpit?.mount) return
  // frame the whole app row: warm page bg + 8px gutter, siblings become
  // the floating rounded panel (cockpit.css .nc-frame-host, desktop only)
  host.value.parentElement?.classList.add("nc-frame-host")
  window.NeoCockpit.mount(host.value, {
    env: "spa",
    layout: "sidebar",
    surfaceApp: props.surfaceApp,
    contextNav: props.contextNav,
    contextFooter: props.contextFooter,
    onSearch: props.onSearch || undefined,
    searchKbd: props.searchKbd || undefined,
    onNavigate: (route) => {
      if (!route) return
      if (route.startsWith("/app") || route.startsWith("http")) {
        window.location.href = route
      } else {
        props.navigate(route)
      }
    },
  })
  mounted = true
}

onMounted(async () => {
  try {
    await loadBoot()
    if (window.frappe?.boot?.neoffice_cockpit_disable) return
    await loadBundle()
    render()
  } catch (e) {
    // never break the host app over chrome — the native sidebar fallback
    // is handled by the parent (v-if on bridgeFailed)
    console.warn("[neocockpit] bridge failed, keeping native sidebar", e)
    emitFailed()
  }
})

const emit = defineEmits(["failed"])
function emitFailed() {
  emit("failed")
}

// Live updates: route changes (active flags) + badge/teams refreshes.
//
// Calling render() again means window.NeoCockpit.mount() on a host that is
// already mounted, with no unmount in between. That is deliberate and it does
// NOT leak a React root: mount() keeps a WeakMap of Root objects keyed by the
// host element and only calls createRoot() when the element has none —
// otherwise it reuses the cached Root and just calls root.render(), which is a
// plain React re-render. Verified 2026-09-04 both in the library source
// (frappe-sidebar-react/src/mount.tsx) and in the bundle we actually ship
// (frappe/public/js/lib/neocockpit.global.js, where it minifies to
// `let a=As.get(e); a||(a=createRoot(e),As.set(e,a)), a.render(...)` with
// `As=new WeakMap`), and on screen: mounting twice on the same host returns
// the identical Root, and eight CRM navigations left the host with exactly one
// __reactContainer key and one child node throughout.
//
// So re-mounting IS the update path here — do not "fix" it by unmounting
// first, which would throw away React state on every navigation.
watch(
  () => [props.contextNav, props.contextFooter],
  () => {
    if (mounted) render()
  },
  { deep: true }
)

onUnmounted(() => {
  if (host.value && window.NeoCockpit?.unmount) {
    host.value.parentElement?.classList.remove("nc-frame-host")
    window.NeoCockpit.unmount(host.value)
  }
})
</script>
