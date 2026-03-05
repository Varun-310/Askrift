import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const client = axios.create({
    baseURL: `${API_URL}/api`,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Auth token interceptor
client.interceptors.request.use((config) => {
    const token = localStorage.getItem('askrift_token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// Response error handler
client.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('askrift_token')
            localStorage.removeItem('askrift_user')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

export default client
export { API_URL }
