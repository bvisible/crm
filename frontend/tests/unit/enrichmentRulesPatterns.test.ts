//// Neoffice — added file (no upstream equivalent): pins the v15 workaround of
//// useEnrichmentRules (#1840) — the rules are listed without the inline child
//// table, which Frappe v15's get_list cannot serve, and their patterns come from
//// a second get_list on the child doctype.
import { describe, it, expect, vi, beforeEach } from 'vitest'

const listOptions: { current: any } = { current: null }
const call = vi.fn()

vi.mock('frappe-ui', () => ({
  call: (...args: unknown[]) => call(...args),
  useList: (options: any) => {
    listOptions.current = options
    return {
      loading: false,
      error: null,
      hasNextPage: false,
      // What frappe-ui does: the rows reach onSuccess before reload resolves.
      reload: async () => {
        options.onSuccess([
          { name: 'Social-0001', enabled: 1 },
          { name: 'Social-0002', enabled: 0 },
        ])
      },
    }
  },
}))

import { useEnrichmentRules } from '@/components/Settings/Enrichment/useEnrichmentRules'

function options(buildRow: any) {
  return {
    ruleType: 'Social' as const,
    fields: ['target_value' as const],
    buildRow,
    newRow: () => ({}),
    isRowChanged: () => false,
    validateRow: () => true,
    toInsert: () => ({}),
    toUpdate: () => ({}),
    clearErrors: () => {},
    messages: { insertError: '', updateError: '', deleteError: '' },
  } as any
}

describe('useEnrichmentRules patterns', () => {
  beforeEach(() => {
    call.mockReset()
  })

  it('never asks the list for the child table inline', () => {
    useEnrichmentRules(options(() => ({})))
    expect(listOptions.current.fields).toEqual(['name', 'enabled', 'target_value'])
    expect(
      listOptions.current.fields.every((field: unknown) => typeof field === 'string'),
    ).toBe(true)
  })

  it('hands each rule its own patterns, in order, once load resolves', async () => {
    call.mockResolvedValue([
      { name: 'p3', parent: 'Social-0002', pattern: 'b', is_regex: 1, idx: 1 },
      { name: 'p2', parent: 'Social-0001', pattern: 'a2', is_regex: 0, idx: 2 },
      { name: 'p1', parent: 'Social-0001', pattern: 'a1', is_regex: 1, idx: 1 },
    ])
    const seen: Record<string, string[]> = {}
    const hook = useEnrichmentRules(
      options((rule: any, patterns: any[]) => {
        seen[rule.name] = patterns.map((pattern) => pattern.pattern)
        return {}
      }),
    )

    expect(await hook.load()).toBe(true)

    expect(call).toHaveBeenCalledWith(
      'frappe.client.get_list',
      expect.objectContaining({
        doctype: 'CRM Enrichment Rule Pattern',
        parent: 'CRM Enrichment Rule',
        filters: { parent: ['in', ['Social-0001', 'Social-0002']] },
      }),
    )
    expect(seen).toEqual({ 'Social-0001': ['a1', 'a2'], 'Social-0002': ['b'] })
    expect(hook.rows.value).toHaveLength(2)
  })

  it('reports a failed pattern fetch as a failed load', async () => {
    call.mockRejectedValue(new Error('boom'))
    const hook = useEnrichmentRules(options(() => ({})))

    expect(await hook.load()).toBe(false)
    expect(hook.error.value).toBeTruthy()
  })
})
