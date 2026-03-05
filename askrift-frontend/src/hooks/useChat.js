import { useState, useCallback, useRef } from 'react'
import { API_URL } from '../api/client'

export function useChat() {
    const [messages, setMessages] = useState([])
    const [isStreaming, setIsStreaming] = useState(false)
    const [streamingText, setStreamingText] = useState('')
    const [citations, setCitations] = useState([])
    const abortRef = useRef(null)

    const sendQuery = useCallback(async (question, activeDocIds = []) => {
        // Add user message
        const userMsg = { role: 'user', content: question }
        setMessages((prev) => [...prev, userMsg])
        setIsStreaming(true)
        setStreamingText('')
        setCitations([])

        // Build conversation history (last 6 exchanges = 12 messages)
        const history = messages.slice(-12).map((m) => ({
            role: m.role,
            content: m.content,
        }))

        try {
            const token = localStorage.getItem('askrift_token')
            const response = await fetch(`${API_URL}/api/chat/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    question,
                    active_doc_ids: activeDocIds,
                    conversation_history: history,
                }),
            })

            if (!response.ok) throw new Error('Query failed')

            const reader = response.body.getReader()
            const decoder = new TextDecoder()
            let fullText = ''
            let finalCitations = []

            while (true) {
                const { done, value } = await reader.read()
                if (done) break

                const chunk = decoder.decode(value, { stream: true })
                const lines = chunk.split('\n')

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6)
                        try {
                            const parsed = JSON.parse(data)
                            if (parsed.type === 'token') {
                                fullText += parsed.content
                                setStreamingText(fullText)
                            } else if (parsed.type === 'citations') {
                                finalCitations = parsed.citations
                            } else if (parsed.type === 'done') {
                                // Stream complete
                            }
                        } catch {
                            // Plain text token
                            fullText += data
                            setStreamingText(fullText)
                        }
                    }
                }
            }

            // Finalize: add assistant message to history
            const assistantMsg = {
                role: 'assistant',
                content: fullText,
                citations: finalCitations,
            }
            setMessages((prev) => [...prev, assistantMsg])
            setCitations(finalCitations)
        } catch (err) {
            console.error('Chat error:', err)
            setMessages((prev) => [
                ...prev,
                { role: 'assistant', content: 'An error occurred. Please try again.', citations: [] },
            ])
        } finally {
            setIsStreaming(false)
            setStreamingText('')
        }
    }, [messages])

    const clearChat = useCallback(() => {
        setMessages([])
        setCitations([])
        setStreamingText('')
        setIsStreaming(false)
    }, [])

    return {
        messages,
        isStreaming,
        streamingText,
        citations,
        sendQuery,
        clearChat,
    }
}
