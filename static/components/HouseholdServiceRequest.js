import ResidentHome from './ResidentHome.js'
import AdminHome from './AdminHome.js'
import ServiceProviderHome from './ProfessionalHome.js'
import HouseholdServiceRequest from './HouseholdServiceRequest.js'

export default {
  template: `<div>
  <ResidentHome v-if="userRole=='resident'"/>
  <AdminHome v-if="userRole=='admin'" />
  <ServiceProviderHome v-if="userRole=='provider'" />
  <HouseholdServiceRequest v-for="(request, index) in requests" :key='index' :request="request" />
  </div>`,

  data() {
    return {
      userRole: localStorage.getItem('role'),
      authToken: localStorage.getItem('auth-token'),
      requests: [],
    }
  },

  components: {
    ResidentHome,
    AdminHome,
    ServiceProviderHome,
    HouseholdServiceRequest,
  },
  async mounted() {
    const res = await fetch('/api/household_service_requests', {
      headers: {
        'Authentication-Token': this.authToken,
      },
    })
    const data = await res.json()
    if (res.ok) {
      this.requests = data
    } else {
      alert(data.message)
    }
  },
}
