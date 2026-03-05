import { motion } from 'framer-motion'
import CitationPill from './CitationPill'

export default function MessageBlock({ message }) {
    const isUser = message.role === 'user'

    return (
        <motion.div
            className="message-block"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
        >
            <div className={`message-label ${isUser ? 'query' : 'answer'}`}>
                {isUser ? 'QUERY' : 'ASKRIFT'}
            </div>
            <div className="message-text">
                {message.content.split('\n').map((line, i) => (
                    <p key={i}>{line}</p>
                ))}
            </div>

            {!isUser && message.citations && message.citations.length > 0 && (
                <div className="citations">
                    {message.citations.map((citation, i) => (
                        <CitationPill key={i} citation={citation} />
                    ))}
                </div>
            )}
        </motion.div>
    )
}
