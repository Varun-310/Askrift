import { motion } from 'framer-motion'

export default function DocumentLibrary({ documents, activeDocIds, onToggle, onDelete }) {
    const getFileType = (name) => {
        const ext = name.split('.').pop().toLowerCase()
        if (ext === 'pdf') return 'PDF'
        if (ext === 'docx' || ext === 'doc') return 'DOC'
        return 'TXT'
    }

    const formatDate = (dateStr) => {
        const d = new Date(dateStr)
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }

    return (
        <aside className="library-panel">
            <div className="library-header">
                <span className="library-title">Documents</span>
                <span className="library-count">{documents.length}</span>
            </div>

            <div className="library-list">
                {documents.length === 0 ? (
                    <div style={{
                        padding: '24px',
                        textAlign: 'center',
                        fontFamily: 'var(--font-mono)',
                        fontSize: '12px',
                        color: 'var(--text-muted)',
                    }}>
                        no documents yet
                    </div>
                ) : (
                    documents.map((doc, i) => (
                        <motion.div
                            key={doc.id}
                            className={`doc-card ${activeDocIds.includes(doc.id) ? 'active' : ''}`}
                            onClick={() => onToggle(doc.id)}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: i * 0.05, duration: 0.2 }}
                        >
                            <span className="doc-card-type">{getFileType(doc.name)}</span>
                            <div className="doc-card-info">
                                <div className="doc-card-name">{doc.name}</div>
                                <div className="doc-card-meta">
                                    {doc.page_count} pages · {formatDate(doc.uploaded_at)}
                                </div>
                            </div>
                            <button
                                className="doc-card-delete"
                                onClick={(e) => {
                                    e.stopPropagation()
                                    onDelete(doc.id)
                                }}
                                title="Delete document"
                            >
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                                    <line x1="18" y1="6" x2="6" y2="18" />
                                    <line x1="6" y1="6" x2="18" y2="18" />
                                </svg>
                            </button>
                        </motion.div>
                    ))
                )}
            </div>
        </aside>
    )
}
