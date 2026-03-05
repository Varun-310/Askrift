import { useState, useCallback } from 'react'
import client from '../api/client'

export function useDocuments() {
    const [documents, setDocuments] = useState([])
    const [activeDocIds, setActiveDocIds] = useState([])
    const [uploading, setUploading] = useState(false)
    const [uploadProgress, setUploadProgress] = useState(0)
    const [loading, setLoading] = useState(false)

    const fetchDocuments = useCallback(async () => {
        setLoading(true)
        try {
            const { data } = await client.get('/documents/list')
            setDocuments(data.documents || [])
        } catch (err) {
            console.error('Failed to fetch documents:', err)
        } finally {
            setLoading(false)
        }
    }, [])

    const uploadDocument = useCallback(async (file) => {
        setUploading(true)
        setUploadProgress(0)
        try {
            const formData = new FormData()
            formData.append('file', file)
            const { data } = await client.post('/documents/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                onUploadProgress: (e) => {
                    const pct = Math.round((e.loaded * 100) / e.total)
                    setUploadProgress(pct)
                },
            })
            await fetchDocuments()
            return data
        } catch (err) {
            console.error('Upload failed:', err)
            throw err
        } finally {
            setUploading(false)
            setUploadProgress(0)
        }
    }, [fetchDocuments])

    const deleteDocument = useCallback(async (docId) => {
        try {
            await client.delete(`/documents/${docId}`)
            setDocuments((prev) => prev.filter((d) => d.id !== docId))
            setActiveDocIds((prev) => prev.filter((id) => id !== docId))
        } catch (err) {
            console.error('Delete failed:', err)
            throw err
        }
    }, [])

    const toggleDocFilter = useCallback((docId) => {
        setActiveDocIds((prev) =>
            prev.includes(docId)
                ? prev.filter((id) => id !== docId)
                : [...prev, docId]
        )
    }, [])

    return {
        documents,
        activeDocIds,
        uploading,
        uploadProgress,
        loading,
        fetchDocuments,
        uploadDocument,
        deleteDocument,
        toggleDocFilter,
    }
}
