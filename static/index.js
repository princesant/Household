export default {
    template: `<div>
    <h1>Manage Household Service Requests</h1>
    <table>
      <thead>
        <tr>
          <th>Request ID</th>
          <th>Service Type</th>
          <th>Description</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request.id">
          <td>{{ request.id }}</td>
          <td>{{ request.service_type }}</td>
          <td>{{ request.description }}</td>
          <td>{{ request.completed ? 'Completed' : 'Pending' }}</td>
          <td>
            <button v-if="!request.completed" @click="markCompleted(request.id)">
              Mark as Completed
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    </div>`,
  
    data() {
      return {
        requests: [],
      }
    },
  
    async mounted() {
      const res = await fetch('/api/household_service_requests', {
        headers: {
          'Authentication-Token': localStorage.getItem('auth-token'),
        },
      })
      const data = await res.json()
      if (res.ok) {
        this.requests = data
      } else {
        alert(data.message)
      }
    },
  
    methods: {
      async markCompleted(requestId) {
        const res = await fetch(`/api/household_service_requests/${requestId}/complete`, {
          method: 'POST',
          headers: {
            'Authentication-Token': localStorage.getItem('auth-token'),
          },
        })
        const data = await res.json()
        if (res.ok) {
          alert('Request marked as completed!')
          this.requests = this.requests.map((req) =>
            req.id === requestId ? { ...req, completed: true } : req
          )
        } else {
          alert(data.message)
        }
      },
    },
  }
  
