import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'

const ACCEPTED_TYPES = {
    'application/pdf': ['.pdf'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'text/plain': ['.txt'],
}

const MAX_SIZE = 20 * 1024 * 1024 // 20MB

export default function UploadZone({ onUpload, onClose, uploading, progress }) {
    const [error, setError] = useState(null)

    const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
        setError(null)
        if (rejectedFiles.length > 0) {
            const err = rejectedFiles[0].errors[0]
            if (err.code === 'file-too-large') {
                setError('File exceeds 20MB limit')
            } else if (err.code === 'file-invalid-type') {
                setError('Unsupported format. Use PDF, DOCX, or TXT')
            } else {
                setError(err.message)
            }
            return
        }
        if (acceptedFiles.length > 0) {
            onUpload(acceptedFiles[0])
        }
    }, [onUpload])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: ACCEPTED_TYPES,
        maxSize: MAX_SIZE,
        multiple: false,
        disabled: uploading,
    })

    return (
        <motion.div
            className="upload-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={(e) => {
                if (e.target === e.currentTarget && !uploading) onClose()
            }}
        >
            <button
                className="upload-close"
                onClick={onClose}
                disabled={uploading}
                id="upload-close"
            >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
            </button>

            <motion.div
                initial={{ opacity: 0, y: -40 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -40 }}
                transition={{ duration: 0.3, ease: 'easeOut' }}
            >
                <div
                    {...getRootProps()}
                    className={`upload-zone ${isDragActive ? 'drag-over' : ''}`}
                    id="upload-dropzone"
                >
                    <input {...getInputProps()} />

                    <svg
                        className="upload-zone-icon"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="17 8 12 3 7 8" />
                        <line x1="12" y1="3" x2="12" y2="15" />
                    </svg>

                    {uploading ? (
                        <>
                            <p className="upload-zone-text">uploading...</p>
                            <div className="upload-progress" style={{ width: '200px', marginTop: '8px' }}>
                                <div className="upload-progress-bar" style={{ width: `${progress}%` }} />
                            </div>
                        </>
                    ) : (
                        <>
                            <p className="upload-zone-text">
                                {isDragActive ? 'release to upload' : 'drop a document or click to browse'}
                            </p>
                            <p className="upload-zone-formats">pdf · docx · txt · max 20mb</p>
                        </>
                    )}

                    {error && (
                        <p style={{
                            fontFamily: 'var(--font-mono)',
                            fontSize: '12px',
                            color: 'var(--danger)',
                            marginTop: '8px',
                        }}>
                            {error}
                        </p>
                    )}
                </div>
            </motion.div>
        </motion.div>
    )
}
