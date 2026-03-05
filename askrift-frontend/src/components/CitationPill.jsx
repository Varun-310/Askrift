import { motion } from 'framer-motion'

export default function CitationPill({ citation }) {
    return (
        <motion.span
            className="citation-pill"
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.15 }}
        >
            <span className="citation-pill-icon">📄</span>
            {citation.doc_name} · p.{citation.page_number}
        </motion.span>
    )
}
