export default {
    template: `<div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <label>Email:</label>
      <input type="email" v-model="email" required />
      <label>Password:</label>
      <input type="password" v-model="password" required />
      <button type="submit">Login</button>
    </form>
    </div>`,
  
    data() {
      return {
        email: '',
        password: '',
      }
    },
    methods: {
      async login() {
        const res = await fetch('/user-login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email: this.email, password: this.password }),
        })
  
        const data = await res.json()
        if (res.ok) {
          localStorage.setItem('auth-token', data.token)
          localStorage.setItem('role', data.role)
          alert('Login successful!')
          window.location.reload()
        } else {
          alert(data.message)
        }
      },
    },
  }
  