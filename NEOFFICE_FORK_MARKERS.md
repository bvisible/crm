# Neoffice fork markers

Everything Neoffice changed in this fork carries a `//// Neoffice` comment saying **why**
(`grep -rn "////"` maps the whole divergence). This file holds what a comment cannot reach:
files with no comment syntax, build artifacts, and hunks where a comment would change the
output. Read it before merging upstream.

Tooling: `bvisible/neoffice-ci` → `scripts/fork_markers.py`
(`check --base <BASE> --head <HEAD>`, `verify --base <sha>`), driven by the
`Fork markers` workflow on every push to `version-15`.

---

## crm

Fork `bvisible/crm`, branch `version-15`. Upstream `frappe/crm` (default branch `develop`;
we track `main`).

### Base and attribution — measured 2026-09-04

| | |
|---|---|
| **BASE** | `9335743ce46b69b79b86adcafff77a1ef925905b` — upstream tag **`v1.56.3`**, *"chore(release): Bumped to Version 1.56.3"*, 2025-11-19 |
| How it was chosen | No upstream branch tip is contained in ours (`git merge-base --is-ancestor` fails for `develop`, `main`, `main-hotfix`, `desk-v2`, `erpnext-sync`). The merge-base with `upstream/main` **and** with `upstream/main-hotfix` is that same commit, and it is the highest one: it leaves 40 commits on our side against 1818 for the merge-base with `develop`. It is also exactly a release tag, so the base is a published upstream state, not a mid-branch point. |
| Ours since BASE | **40 commits** — `git rev-list --count origin/version-15 ^BASE` = 40, and `--not $(git for-each-ref refs/remotes/upstream refs/tags)` gives the same 40: not one upstream commit is attributed to us. Authors: Jérémy Christillin ×36, `github-actions[bot]` ×4 (the committed frontend builds). |
| Cherry-picks from upstream | **0** — no `(cherry picked from commit …)` line in the range. Nothing here is an upstream backport. |
| Diff BASE..HEAD | 186 files, +9199 / −2566 — of which 149 files are the committed SPA build under `crm/public/frontend/`. |
| Spot-checked with `git blame` (not `-w`) | `.gitignore:9`, `frontend/src/socket.js:5`, `Apps.vue:59`, `index.css:25`, `components.d.ts:202`, `vite.config.js:83`, `crm/public/images/logo.svg:1` — every one blames to one of our 40 commits. |

**The divergence is entirely frontend, build and i18n.** `git diff BASE..HEAD -- 'crm/**/*.py'
'crm/**/*.json'` (excluding the built SPA) is **empty**: no Python, no DocType JSON, no
fixture, no permission rule. There is nothing of ours in the CRM backend.

### Files that cannot carry a comment

| Path | What we changed | At the merge |
|---|---|---|
| `package.json` | `build` became a guard: skip `yarn build` when `crm/public/frontend/assets` already exists, unless `FORCE_REBUILD=1`; the real build moved to `build:force`. Reason: the artifacts are committed (see below), so an instance must never rebuild. Commit `f303b6ed`. | Keep ours, re-apply upstream's other scripts. |
| `frontend/package.json` | `build` / `build:force` wrapped in `cross-env NODE_OPTIONS=--max-old-space-size=4096` (the build OOMs on a 4 GB VM); `cross-env ^10.1.0` added to devDependencies; `frappe-ui` pinned to the exact `0.1.201` instead of `^0.1.201` (a floating minor changed the sidebar under us). Commits `d7c4209b`, `9b8eb395`, `aecf7240`. | Keep the pin and the NODE_OPTIONS; take upstream's dependency bumps. |
| `.mcp.json` | **Added file, no upstream equivalent.** Declares two local MCP servers (`po-translation`, `poeditor`) by absolute path under `/Users/jeremy/mcp/`. Machine-specific; the `POEDITOR_API_TOKEN` value is the placeholder `your_token_here_if_you_use_poeditor_com`, not a secret. Added by commit `5afea979` without a word about it in the message. **TO REVIEW: it should probably be deleted** — it is dead on every machine but one and ships to every instance. | Delete rather than merge. |
| `frappe-ui` (git submodule pointer) | Bumped `c9a0fc93` → `3423aa5b` by commit `aecf7240` ("Update FR"), which says nothing about it. **TO REVIEW: origin unknown.** The submodule is only an alias source for local dev (`vite.config.js` adds it only when `isDev`); the shipped build uses the npm `frappe-ui@0.1.201`. | Take upstream's pointer unless local dev needs ours. |
| `crm/locale/fr.po`, `crm/locale/main.pot` | Our French pass (+1893 / −1634 on `fr.po`). See "Known defects". | Merge with the PO tooling (`bench generate-pot-file` / `update-po-files`), never by hand. |
| `crm/locale/fr.mo` | **Added binary — upstream commits no `.mo`.** Build output of `bench compile-po-to-mo`, and one Frappe never reads. **Deleted 2026-09-04**; `crm/locale/*.mo` is now gitignored. | Nothing to merge. |
| `frontend/yarn.lock` | Adds `cross-env@10.1.0` + `@epic-web/invariant@1.0.0`, and pins `frappe-ui@0.1.201`. Follows `frontend/package.json`. | Regenerate from the merged `package.json`, never merge by hand. |
| `crm/public/frontend/**` (149 files) + `crm/public/frontend/index.html` | The committed vite build (JS/CSS chunks, Inter woff2, PWA manifest, `sw.js`, `workbox-*.js`, images). Upstream gitignores all of it. | Never merge: take upstream's sources, then rebuild. |
| `.github/workflows/build-frontend.yml`, `tests.yml`, `upstream-preview.yml`, `fork-markers.yml` | **Added, no upstream equivalent** — the commit-the-build bot and the fleet CI (`bvisible/neoffice-ci`). Upstream's own workflows as of v1.56.3 (`ci.yml`, `builds.yml`, `generate-pot-file.yml`, `on_release.yml`, `release_notes.yml`) are untouched. | Keep ours, take upstream's. Note that upstream has since **dropped `ci.yml`** and split it into `frontend-tests.yml`, `linters.yml`, `migration-test.yml`, `server-tests.yml`, `ui-tests.yml`: at the merge `ci.yml` disappears and five files arrive. No name collides with ours. |

### Build artifacts — mark the source, never the artifact

`crm/www/crm.html` is a **build output**: vite renders `frontend/index.html` into
`crm/public/frontend/index.html`, and `yarn copy-html-entry` copies it to `crm/www/crm.html`.
It was byte-identical to `crm/public/frontend/index.html` before this pass
(`sha256 8875a3b9…`).

The marker for it is written in **`frontend/index.html`** (the source) so that a rebuild
keeps it — HTML comments survive the vite build, as upstream's own `<!-- PWA -->` comment
proves. The same marker was copied by hand into `crm/www/crm.html` so the check is green
today. It could **not** be copied into `crm/public/frontend/index.html`: `fork_markers.py
verify` refuses any added line under a skipped directory. Until the next build bot run those
two files differ by that one comment block; the next `yarn build` makes them identical again.

**Never hand-edit `crm/www/crm.html` or anything under `crm/public/frontend/`.**

### Hunks a comment cannot reach

| Hunk | Why | What to do |
|---|---|---|
| `frappe-ui` — `-Subproject commit c9a0fc93` / `+Subproject commit 3423aa5b` | A submodule gitlink is not a file: `git show HEAD:frappe-ui` fails, so `fork_markers.py` can neither find a marker near it nor accept a manifest entry (the escape hatch only covers `kind == "none"` and binaries). This is the **one hunk of the whole fork that stays red** in a full-history `check --base v1.56.3`. It does not turn the CI red: the `Fork markers` workflow only diffs the pushed range. | Documented here; see the row above for the merge decision. |

### Decisions worth recording

- **Empty `__init__.py`** — none: our divergence adds no Python package, only the ten
  root-level scripts (each carrying its own header marker) and nothing inside `crm/`.
- **`frontend/components.d.ts`** is generated by `unplugin-vue-components`. Upstream commits
  it but had not regenerated it at v1.56.3 (it still listed the deleted
  `Settings/LeadSyncing/*` and was missing `Settings/AssignmentRules/*`,
  `ConditionsFilter/*`, `Icons/SettingsIcon2`). Ours is a fresh regeneration plus our two
  NeoCockpit components. **At the merge: take upstream's file and let the plugin regenerate
  it** — the markers go away with it.
- No file in the divergence is identical-but-for-whitespace, except the very end of
  `frontend/src/socket.js`, where upstream had no final newline and we added one; that is
  marked in place.

### Merge forecast — BASE..`upstream/main` touches 651 files, BASE..`upstream/develop` 731

Changed on **both** sides (identical list for `main` and `develop`), i.e. where conflicts are
expected — the 149 committed build files aside:

| File | Expect |
|---|---|
| `frontend/src/socket.js` | **Hard conflict.** Upstream is likely to have reworked the `common_site_config.json` import itself; ours made `initSocket()` async. Keep async, re-apply upstream's socket logic inside it. |
| `frontend/src/main.js` | Follows `socket.js`: keep the `.then()` shape. |
| `frontend/src/telemetry.ts` | Upstream may still import `posthog.js` relatively. Keep it removed — **and fix the unguarded `posthog.init` while you are there** (see below). |
| `frontend/vite.config.js` | Keep `sourcemap: false` and the `build.rollupOptions.external` block; take upstream's plugin list. |
| `frontend/src/components/Layouts/DesktopLayout.vue` | Keep `<NeoCockpitCRMSidebar />`; take upstream's other layout changes. |
| `frontend/src/components/Apps.vue` | Keep the removal of the hardcoded Desk tile. |
| `frontend/src/index.css` | Ours is purely additive at the end of the file — take both sides. |
| `frontend/components.d.ts` | Take upstream's, regenerate. |
| `package.json`, `frontend/package.json`, `frontend/yarn.lock` | Take upstream's dependencies, re-apply our three build decisions (skip-if-built, NODE_OPTIONS, frappe-ui pin). |
| `crm/locale/fr.po`, `crm/locale/main.pot` | Regenerate the POT, then `update-po-files`. |
| `.gitignore`, `README.md`, `frappe-ui` | Small, keep both sides' intent. |

**No DocType JSON conflict is possible** — we changed none. Nothing here needs to become a
Custom Field.

Upstream also added five locales after v1.56.3 (`bg`, `hi`, `ko`, `sl`, `uz`); they are simply
new files, not a divergence.

### Known defects found while marking — NOT fixed here

1. ~~**`crm/locale/fr.mo` is committed and stale.**~~ **Fixed 2026-09-04 — and the
   diagnosis above it was wrong.** The file was real (877 entries against 1338 in `fr.po`)
   but it was **never read**: `frappe/gettext/translate.py` resolves catalogues through
   `get_translations_from_mo()` -> `gettext.find(app, get_locale_dir(), (lang,))`, and
   `get_locale_dir()` is `<bench>/sites/assets/locale`, *not* the app directory. The MO the
   fleet actually serves is `sites/assets/locale/fr/LC_MESSAGES/crm.mo`, written by
   `compile_translations()` — which `bench compile-po-to-mo` runs, and which `bench build`
   also runs at the end of every build, so `bench get-app` (-> `build_assets()` ->
   `bench build --app crm`) already produces it on a fresh install. Verified on osiris:
   that MO holds the full 1338 entries, and msgids absent from the committed `fr.mo`
   (e.g. `File "{0}" was skipped because of invalid file type`) resolve in French through
   `frappe.translate.get_all_translations("fr")`. No French string was ever missing.
   The file was deleted and `crm/locale/*.mo` gitignored: a committed build artifact that
   nothing reads can only drift and mislead, as this one did.
2. **`frontend/src/telemetry.ts:56` and `:78`** — `posthog.init(…)` and
   `window.posthog.capture(…)` are unguarded, while `posthog` is bound once at module load
   from `window.posthog`. Commit `c23157ba` removed the only import that defined
   `window.posthog`, and `posthogPlugin` (`:90`) calls `posthogSettings.fetch()` precisely
   *because* `window.posthog` is undefined — so on any site where Frappe returns
   `enable_telemetry` with a project id and host, `initPosthog` throws
   `TypeError: Cannot read properties of undefined (reading 'init')`. The comment in the file
   claiming "telemetry is a no-op" is not what the code does.
3. **Ten one-off PO scripts at the repo root** (`translate_po.py`, `translate_crm_po.py`,
   `complete_translation.py`, `complete_all_translations.py`, `complete_fr_translation.py`,
   `apply_translations.py`, `final_translations.py`, `last_translations.py`,
   `translate_all_with_mcp.py`, `translate_with_mcp.py` — ~5100 lines). They hardcode
   `/Users/jeremy/GitHub/crm`, rewrite the PO by regex instead of using
   `generate-pot-file` / `update-po-files` / `compile-po-to-mo`, and ship to every instance
   with the app. Commit `5afea979` added nine of them under a message about frontend assets.
4. **`.mcp.json`** — see the table: a repo-root MCP config, auto-loaded by any Claude Code
   session that clones this repo, pointing at two servers under `/Users/jeremy/mcp/`.
5. **`NeoCockpitBridge.vue`** — the `watch` on `contextNav` calls `render()` again, i.e.
   `window.NeoCockpit.mount(host, …)` on the same host node without a preceding `unmount`.
   CRM's `contextNav` is a `computed` that changes on **every route change** (the `active`
   flags), so this fires on every navigation. Whether it leaks a React root per navigation
   depends on the bundle (which lives in `frappe`, not here) — **unverified**, worth a look.
6. **`NeoCockpitCRMSidebar.vue`** — `active` is computed with
   `String(route.name).startsWith(item.to)`, so a detail route (`Lead`, `Deal`, `Contact`)
   never highlights its list entry (`Leads`, `Deals`, `Contacts`): the test runs the wrong
   way round. Cosmetic.
7. **`frontend/src/socket.js`** — the dev-only dynamic import uses the deprecated
   `{ assert: { type: 'json' } }` form; modern runtimes want `{ with: … }`. Harmless under
   Vite 4 today (and it is inside a `try`), but it is a shape that will break.
