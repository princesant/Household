export default {
    template: `<div>
    <h1>Request a Household Service</h1>
    <form @submit.prevent="submitRequest">
      <label>Service Type:</label>
      <input type="text" v-model="serviceType" required />
      <label>Description:</label>
      <textarea v-model="description" required></textarea>
      <button type="submit">Submit</button>
    </form>
    </div>`,
  
    data() {
      return {
        serviceType: '',
        description: '',
      }
    },
    methods: {
      async submitRequest() {
        const res = await fetch('/api/household_service_requests', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('auth-token'),
          },
          body: JSON.stringify({
            service_type: this.serviceType,
            description: this.description,
          }),
        })
  
        const data = await res.json()
        if (res.ok) {
          alert('Service request submitted successfully!')
          this.serviceType = ''
          this.description = ''
        } else {
          alert(data.message)
        }
      },
    },
  }
  