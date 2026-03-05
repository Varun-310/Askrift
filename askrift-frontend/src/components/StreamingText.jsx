export default function StreamingText({ text }) {
    return (
        <span>
            {text}
            <span className="streaming-cursor" />
        </span>
    )
}
