//// Neoffice — upstream's second line was
//// import { socketio_port } from '../../../../sites/common_site_config.json'
//// — a module-scope reach into the bench that only resolves when the app sits
//// inside a frappe-bench, so the standalone / CI build died on it. The read
//// moved inside initSocket() behind import.meta.env.DEV, which is why the
//// function became async. Commit a274058b.
import { io } from 'socket.io-client'
import { getCachedListResource } from 'frappe-ui/src/resources/listResource'
import { getCachedResource } from 'frappe-ui/src/resources/resources'

export async function initSocket() {
  //// Neoffice — see the note at the top of this file (commit a274058b).
  // Default to the standard Frappe socketio port. In dev we try to read the
  // bench's common_site_config.json (which is only available when the repo is
  // checked out inside frappe-bench), otherwise we fall back to the default.
  // In production the value is provided by window.socketio_port if needed.
  let socketio_port = '9000'

  if (import.meta.env.DEV) {
    try {
      //// Neoffice — this dynamic import is ours (commit a274058b); `assert`
      //// is the pre-standard spelling of what is now Import Attributes
      //// (`with`). It STAYS until this app leaves Vite 4: that toolchain
      //// (esbuild 0.18, rollup 3) predates import attributes, so `with` is
      //// the spelling it would not recognise — not the other way round.
      //// Nothing depends on the attribute today in any case: Vite serves
      //// `.json` as a JS module, the branch is dev-only, and the import sits
      //// in a try/catch that falls back to the default port. Remove this note
      //// and switch to `with: { type: 'json' }` when frontend/package.json
      //// moves to Vite 5+ / Rollup 4+.
      const cfg = await import('../../../../sites/common_site_config.json', {
        assert: { type: 'json' },
      })
      socketio_port = cfg.socketio_port || socketio_port
    } catch {
      console.log("You have not set a default site, sockets won't work in dev.")
    }
  }

  let host = window.location.hostname
  let siteName = window.site_name
  //// Neoffice — window.socketio_port (injected by the Frappe page) now wins
  //// over the local default; upstream used the value read from the bench
  //// config at module scope. Commit a274058b.
  let port = window.location.port ? `:${window.socketio_port || socketio_port}` : ''
  let protocol = port ? 'http' : 'https'
  let url = `${protocol}://${host}${port}/${siteName}`

  let socket = io(url, {
    withCredentials: true,
    reconnectionAttempts: 5,
  })
  socket.on('refetch_resource', (data) => {
    if (data.cache_key) {
      let resource =
        getCachedResource(data.cache_key) ||
        getCachedListResource(data.cache_key)
      if (resource) {
        resource.reload()
      }
    }
  })
  return socket
  //// Neoffice — the file now ends with a newline; upstream's ended without one,
  //// which is the whole of the change on the closing brace below. Commit
  //// a274058b.
}
