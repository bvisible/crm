//// Neoffice — upstream's first line was
//// import '../../../frappe/frappe/public/js/lib/posthog.js' — a relative reach
//// into the frappe app that 404s in production (frappe's public assets are not
//// served under /assets/frappe/frappe/public/). Removed: posthog is read from
//// window when the host page provides it, and telemetry is a no-op otherwise.
//// Commit c23157ba.
import { createResource } from 'frappe-ui'

// NOTE: the legacy `import '../../../frappe/frappe/public/js/lib/posthog.js'`
// was removed because the externalised path 404s in production (the
// frappe public assets are not served at /assets/frappe/frappe/public/...).
// Posthog is now expected to be loaded by the host page (Frappe core injects
// window.posthog via the desk-side bundle); when absent, telemetry is a no-op.

declare global {
  interface Window {
    posthog: any
  }
}
type PosthogSettings = {
  posthog_project_id: string
  posthog_host: string
  enable_telemetry: boolean
  telemetry_site_age: number
}
interface CaptureOptions {
  data: {
    user: string
    [key: string]: string | number | boolean | object
  }
}

let posthog: typeof window.posthog = window.posthog

// Posthog Settings
let posthogSettings = createResource({
  url: 'crm.api.get_posthog_settings',
  cache: 'posthog_settings',
  onSuccess: (ps: PosthogSettings) => initPosthog(ps),
})

let isTelemetryEnabled = () => {
  if (!posthogSettings.data) return false

  return (
    posthogSettings.data.enable_telemetry &&
    posthogSettings.data.posthog_project_id &&
    posthogSettings.data.posthog_host
  )
}

// Posthog Initialization
function initPosthog(ps: PosthogSettings) {
  if (!isTelemetryEnabled()) return

  posthog.init(ps.posthog_project_id, {
    api_host: ps.posthog_host,
    person_profiles: 'identified_only',
    autocapture: false,
    capture_pageview: true,
    capture_pageleave: true,
    enable_heatmaps: false,
    disable_session_recording: true,
    advanced_disable_decide: true,
    loaded: (ph: typeof posthog) => {
      window.posthog = ph
      ph.identify(window.location.hostname)
    },
  })
}

// Posthog Functions
function capture(
  event: string,
  options: CaptureOptions = { data: { user: '' } },
) {
  if (!isTelemetryEnabled()) return
  window.posthog.capture(`crm_${event}`, options)
}

function startRecording() {
}

function stopRecording() {
}

// Posthog Plugin
function posthogPlugin(app: any) {
  app.config.globalProperties.posthog = posthog
  if (!window.posthog?.length) posthogSettings.fetch()
}

export {
  posthog,
  posthogSettings,
  posthogPlugin,
  capture,
  startRecording,
  stopRecording,
}
