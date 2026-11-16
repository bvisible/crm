// //// Neoffice — added file (no upstream equivalent)
// //// The pages that apps add to the CRM's menu (`crm.api.extension_tabs.get_pages`): the hub's managers read the funnel of
// //// their representatives' visits and issue their cards there. Empty on a site where no app adds one.
import { defineStore } from 'pinia'
import { createResource } from 'frappe-ui'

export const extensionPagesStore = defineStore('crm-extension-pages', () => {
  const pages = createResource({
    url: 'crm.api.extension_tabs.get_pages',
    cache: 'crm_extension_pages',
    initialData: [],
    auto: true,
  })

  function getPage(name) {
    return (pages.data || []).find((page) => page.name === name)
  }

  return { pages, getPage }
})
