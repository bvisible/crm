import ContactsIcon from '@/components/Icons/ContactsIcon.vue'
import DealsIcon from '@/components/Icons/DealsIcon.vue'
import LeadsIcon from '@/components/Icons/LeadsIcon.vue'
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import OrganizationsIcon from '@/components/Icons/OrganizationsIcon.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import TaskIcon from '@/components/Icons/TaskIcon.vue'
import LucideLayoutDashboard from '~icons/lucide/layout-dashboard'
import router from '@/router'
//// Neoffice — the store of the users, for the menu of a sales representative (see below)
import { usersStore } from '@/stores/users'

export const navigationItems = [
  {
    label: 'Dashboard',
    icon: LucideLayoutDashboard,
    route: 'Dashboard',
    desktopOnly: true,
  },
  { label: 'Leads', icon: LeadsIcon, route: 'Leads' },
  { label: 'Deals', icon: DealsIcon, route: 'Deals' },
  { label: 'Contacts', icon: ContactsIcon, route: 'Contacts' },
  { label: 'Organizations', icon: OrganizationsIcon, route: 'Organizations' },
  { label: 'Notes', icon: NoteIcon, route: 'Notes' },
  { label: 'Tasks', icon: TaskIcon, route: 'Tasks' },
  { label: 'Call Logs', icon: PhoneIcon, route: 'Call Logs' },
]

// //// Neoffice — a sales representative reaches their prospects, their notes, tasks and calls, and nothing of the house's deals,
// //// contacts or organizations (the hub gives them no right on those): their entries are left out of the menu and the palette.
export const HIDDEN_FOR_REPRESENTATIVES = ['Deals', 'Contacts', 'Organizations']

export function getNavigationItems({ mobile = false } = {}) {
  //// Neoffice — is the account a sales representative? (their menu leaves out `HIDDEN_FOR_REPRESENTATIVES`)
  const { isRepresentative } = usersStore()
  const representative = isRepresentative()
  //// Neoffice — the filter below keeps the entries that are theirs
  return navigationItems.filter(
    (item) =>
      router.hasRoute(item.route) &&
      (!mobile || !item.desktopOnly) &&
      !(representative && HIDDEN_FOR_REPRESENTATIVES.includes(item.route)),
  )
}
