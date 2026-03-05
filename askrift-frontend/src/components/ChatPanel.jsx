import { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import MessageBlock from './MessageBlock'
import StreamingText from './StreamingText'

export default function ChatPanel({ messages, isStreaming, streamingText, onSendQuery, hasDocuments, onClearChat }) {
    const [input, setInput] = useState('')
    const messagesEndRef = useRef(null)
    const inputRef = useRef(null)

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages, streamingText])

    const handleSubmit = (e) => {
        e.preventDefault()
        if (!input.trim() || isStreaming) return
        onSendQuery(input.trim())
        setInput('')
        inputRef.current?.focus()
    }

    return (
        <main className="chat-panel">
            <div className="chat-messages">
                {messages.length === 0 && !isStreaming && (
                    <div className="empty-state">
                        <div className="empty-state-bg" />
                        <p className="empty-state-text">
                            {hasDocuments
                                ? 'drop a question. get answers.'
                                : 'drop a document. ask anything.'}
                        </p>
                    </div>
                )}

                {messages.map((msg, i) => (
                    <MessageBlock key={i} message={msg} />
                ))}

                {isStreaming && (
                    <motion.div
                        className="message-block"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                    >
                        <div className="message-label answer">ASKRIFT</div>
                        <div className="message-text">
                            <StreamingText text={streamingText} />
                        </div>
                    </motion.div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* ── Input Bar ──────────────────────────── */}
            <form className="input-bar" onSubmit={handleSubmit}>
                <input
                    ref={inputRef}
                    className="input-field"
                    type="text"
                    placeholder={hasDocuments ? 'ask a question about your documents...' : 'upload a document to begin...'}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    disabled={isStreaming}
                    id="chat-input"
                />
                <button
                    className="send-button"
                    type="submit"
                    disabled={!input.trim() || isStreaming}
                    id="send-button"
                >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <line x1="5" y1="12" x2="19" y2="12" />
                        <polyline points="12 5 19 12 12 19" />
                    </svg>
                </button>
            </form>
        </main>
    )
}
