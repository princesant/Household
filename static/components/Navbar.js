export default {
    template: `<nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li v-if="userRole === 'admin'"><a href="/users">Manage Users</a></li>
      <li v-if="authToken"><a @click="logout">Logout</a></li>
    </ul>
    </nav>`,
  
    data() {
      return {
        authToken: localStorage.getItem('auth-token'),
        userRole: localStorage.getItem('role'),
      }
    },
    methods: {
      logout() {
        localStorage.removeItem('auth-token')
        localStorage.removeItem('role')
        alert('Logged out successfully.')
        window.location.reload()
      },
    },
  }
  