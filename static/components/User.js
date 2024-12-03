export default {
    template: `<div>
    <h1>Manage Users</h1>
    <table>
      <thead>
        <tr>
          <th>Email</th>
          <th>Role</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>{{ user.active ? 'Active' : 'Inactive' }}</td>
        </tr>
      </tbody>
    </table>
    </div>`,
  
    data() {
      return {
        users: [],
      }
    },
    async mounted() {
      const res = await fetch('/users', {
        headers: {
          'Authentication-Token': localStorage.getItem('auth-token'),
        },
      })
      const data = await res.json()
      if (res.ok) {
        this.users = data
      } else {
        alert(data.message)
      }
    },
  }
  
