import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createDialog } from './utils/dialogs'
import { initSocket } from './socket'
import router from './router'
import translationPlugin from './translation'
import { posthogPlugin } from './telemetry'
import App from './App.vue'

import {
  FrappeUI,
  Button,
  Input,
  TextInput,
  FormControl,
  ErrorMessage,
  Dialog,
  Alert,
  Badge,
  setConfig,
  frappeRequest,
  FeatherIcon,
} from 'frappe-ui'

let globalComponents = {
  Button,
  TextInput,
  Input,
  FormControl,
  ErrorMessage,
  Dialog,
  Alert,
  Badge,
  FeatherIcon,
}

// create a pinia instance
let pinia = createPinia()

let app = createApp(App)

setConfig('resourceFetcher', frappeRequest)
app.use(FrappeUI)
app.use(pinia)
app.use(router)
app.use(translationPlugin)
app.use(posthogPlugin)
for (let key in globalComponents) {
  app.component(key, globalComponents[key])
}

app.config.globalProperties.$dialog = createDialog

//// Neoffice — initSocket() is async now (see socket.js), so upstream's
//// module-level `let socket` binding and its two synchronous assignments
//// below were replaced by `.then()`. Commit a274058b.

if (import.meta.env.DEV) {
  frappeRequest({ url: '/api/method/crm.www.crm.get_context_for_dev' }).then(
    (values) => {
      for (let key in values) {
        window[key] = values[key]
      }
      //// Neoffice — upstream: socket = initSocket(); then a direct assignment.
      //// initSocket() is async now. Commit a274058b.
      initSocket().then((socket) => {
        app.config.globalProperties.$socket = socket
      })
      app.mount('#app')
    },
  )
} else {
  //// Neoffice — same as the DEV branch above: initSocket() is async now.
  //// Commit a274058b.
  initSocket().then((socket) => {
    app.config.globalProperties.$socket = socket
  })
  app.mount('#app')
}

if (import.meta.env.DEV) {
  window.$dialog = createDialog
}
