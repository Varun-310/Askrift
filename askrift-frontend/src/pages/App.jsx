import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useAuth } from '../hooks/useAuth'
import { useDocuments } from '../hooks/useDocuments'
import { useChat } from '../hooks/useChat'
import DocumentLibrary from '../components/DocumentLibrary'
import ChatPanel from '../components/ChatPanel'
import UploadZone from '../components/UploadZone'

export default function App() {
    const { user, logout } = useAuth()
    const {
        documents,
        activeDocIds,
        uploading,
        uploadProgress,
        fetchDocuments,
        uploadDocument,
        deleteDocument,
        toggleDocFilter,
    } = useDocuments()
    const { messages, isStreaming, streamingText, sendQuery, clearChat } = useChat()
    const [showUpload, setShowUpload] = useState(false)

    useEffect(() => {
        fetchDocuments()
    }, [fetchDocuments])

    const handleSendQuery = (question) => {
        sendQuery(question, activeDocIds)
    }

    const handleUpload = async (file) => {
        try {
            await uploadDocument(file)
            setShowUpload(false)
        } catch (err) {
            console.error('Upload failed:', err)
        }
    }

    return (
        <div className="app-container">
            {/* ── Top Bar ─────────────────────────────── */}
            <motion.header
                className="topbar"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
            >
                <h1 className="topbar-logo">
                    Ask<span>rift</span>
                </h1>

                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <button
                        className="upload-btn"
                        onClick={() => setShowUpload(true)}
                        id="upload-trigger"
                    >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                            <line x1="12" y1="5" x2="12" y2="19" />
                            <line x1="5" y1="12" x2="19" y2="12" />
                        </svg>
                        Upload
                    </button>

                    <button
                        className="upload-btn"
                        onClick={logout}
                        style={{ fontSize: '12px', padding: '6px 12px' }}
                    >
                        Logout
                    </button>
                </div>
            </motion.header>

            {/* ── Workspace ──────────────────────────── */}
            <div className="workspace">
                <motion.div
                    className="stagger-1"
                    style={{ display: 'contents' }}
                >
                    <DocumentLibrary
                        documents={documents}
                        activeDocIds={activeDocIds}
                        onToggle={toggleDocFilter}
                        onDelete={deleteDocument}
                    />
                </motion.div>

                <motion.div
                    className="stagger-2"
                    style={{ display: 'contents' }}
                >
                    <ChatPanel
                        messages={messages}
                        isStreaming={isStreaming}
                        streamingText={streamingText}
                        onSendQuery={handleSendQuery}
                        hasDocuments={documents.length > 0}
                        onClearChat={clearChat}
                    />
                </motion.div>
            </div>

            {/* ── Upload Overlay ─────────────────────── */}
            <AnimatePresence>
                {showUpload && (
                    <UploadZone
                        onUpload={handleUpload}
                        onClose={() => setShowUpload(false)}
                        uploading={uploading}
                        progress={uploadProgress}
                    />
                )}
            </AnimatePresence>
        </div>
    )
}
