import {
  getNavigationItems,
  navigationItems,
  HIDDEN_FOR_REPRESENTATIVES,
} from '@/utils/navigation'

//// Neoffice — the menu of a sales representative (the hub's role) leaves out what is not theirs. The store of the users is
//// simulated: `isRepresentative` is what it answers, and the real rule is `stores/users.js`.
const state = vi.hoisted(() => ({ representative: false }))
vi.mock('@/stores/users', () => ({
  usersStore: () => ({ isRepresentative: () => state.representative }),
}))

describe('navigationItems', () => {
  //// Neoffice — every test starts with an account that is not a representative
  beforeEach(() => {
    state.representative = false
  })

  it('uses unique route names', () => {
    const routes = navigationItems.map((item) => item.route)
    expect(new Set(routes).size).toBe(routes.length)
  })

  it('omits desktop-only destinations on mobile', () => {
    const mobileRoutes = getNavigationItems({ mobile: true }).map(
      (item) => item.route,
    )
    expect(mobileRoutes).not.toContain('Dashboard')
    expect(mobileRoutes).not.toContain('Calendar')
    expect(mobileRoutes).toContain('Leads')
  })

  //// Neoffice — a representative keeps their prospects, notes, tasks and calls, and loses the house's deals, contacts and organizations
  it('leaves out deals, contacts and organizations for a sales representative', () => {
    state.representative = true
    const routes = getNavigationItems().map((item) => item.route)
    for (const hidden of HIDDEN_FOR_REPRESENTATIVES) {
      expect(routes).not.toContain(hidden)
    }
    expect(routes).toContain('Leads')
    expect(routes).toContain('Tasks')
  })

  it('leaves nothing out for anyone else', () => {
    const routes = getNavigationItems().map((item) => item.route)
    for (const hidden of HIDDEN_FOR_REPRESENTATIVES) {
      expect(routes).toContain(hidden)
    }
  })
})
