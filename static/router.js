import Home from './components/Home.js'
import Login from './components/Login.js'
import ServiceRequests from './components/ServiceRequests.js'
import ServiceRequestForm from './components/ServiceRequestForm.js'

const routes = [
    { path: '/', component: Home, name: 'Home' },
    { path: '/login', component: Login, name: 'Login' },
    { path: '/service-requests', component: ServiceRequests, name: 'ServiceRequests' },
    { path: '/create-service-request', component: ServiceRequestForm, name: 'CreateServiceRequest' },
]

export default new VueRouter({
    routes,
})
