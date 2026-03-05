import { useState, useEffect, useCallback } from 'react'
import client from '../api/client'

export function useAuth() {
    const [user, setUser] = useState(() => {
        const saved = localStorage.getItem('askrift_user')
        return saved ? JSON.parse(saved) : null
    })
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const login = useCallback(async (email, password) => {
        setLoading(true)
        setError(null)
        try {
            const { data } = await client.post('/auth/login', { email, password })
            localStorage.setItem('askrift_token', data.token)
            localStorage.setItem('askrift_user', JSON.stringify(data))
            setUser(data)
            return data
        } catch (err) {
            const msg = err.response?.data?.detail || 'Login failed'
            setError(msg)
            throw err
        } finally {
            setLoading(false)
        }
    }, [])

    const register = useCallback(async (name, email, password) => {
        setLoading(true)
        setError(null)
        try {
            const { data } = await client.post('/auth/register', { name, email, password })
            localStorage.setItem('askrift_token', data.token)
            localStorage.setItem('askrift_user', JSON.stringify(data))
            setUser(data)
            return data
        } catch (err) {
            const msg = err.response?.data?.detail || 'Registration failed'
            setError(msg)
            throw err
        } finally {
            setLoading(false)
        }
    }, [])

    const logout = useCallback(() => {
        localStorage.removeItem('askrift_token')
        localStorage.removeItem('askrift_user')
        setUser(null)
    }, [])

    return { user, loading, error, login, register, logout, setError }
}
