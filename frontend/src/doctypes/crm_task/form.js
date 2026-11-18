export class CRMTask {
  onRender() {
    if (this.doc.reference_doctype && this.doc.reference_docname) {
      // //// Neoffice — the English name of the doctype (`reference_doctype.replace('CRM ', '')`) is no longer put in the label of
      // //// the action: upstream built « Open {0} » from it, which no catalogue translates (« Ouvrir Lead »).
      this.actions = [
        {
          name: 'Redirect Action',
          // //// Neoffice — one sentence per target: « Ouvrir le prospect » / « Ouvrir l'affaire »
          label:
            this.doc.reference_doctype == 'CRM Deal'
              ? __('Open deal')
              : __('Open lead'),
          onClick: (close) => {
            if (!this.doc.reference_docname) return
            let name =
              this.doc.reference_doctype == 'CRM Deal' ? 'Deal' : 'Lead'
            let params = { leadId: this.doc.reference_docname }
            if (name == 'Deal') {
              params = { dealId: this.doc.reference_docname }
            }
            this.router.push({ name: name, params: params })
            close?.()
          },
        },
      ]
    }
  }
}
