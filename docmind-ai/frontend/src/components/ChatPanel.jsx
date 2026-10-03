import { Bot, CornerDownLeft, FileText, Send, UserRound } from "lucide-react";

function Message({ message }) {
  const isUser = message.role === "user";
  return (
    <article className={`message ${isUser ? "user-message" : ""}`}>
      <div className={`avatar ${isUser ? "user-avatar" : ""}`}>
        {isUser ? <UserRound size={17} /> : <Bot size={18} />}
      </div>
      <div className="message-body">
        <div className="message-meta">
          <strong>{isUser ? "You" : "DocMind"}</strong>
          {!isUser && <span>AI assistant</span>}
        </div>
        <p>{message.content}</p>
        {message.sources?.length > 0 && (
          <div className="sources">
            <div className="sources-title"><FileText size={14} /> Sources</div>
            {message.sources.map((source, index) => (
              <details className="source-item" key={`${source.page}-${index}`}>
                <summary>Page {source.page}</summary>
                <p>{source.content}</p>
              </details>
            ))}
          </div>
        )}
      </div>
    </article>
  );
}

export default function ChatPanel({
  messages,
  question,
  loading,
  disabled,
  onQuestionChange,
  onSend,
}) {
  return (
    <section className="chat-card">
      <header className="chat-header">
        <div>
          <div className="eyebrow">DOCUMENT RESEARCH</div>
          <h2>Chat with your document</h2>
        </div>
        <div className="secure-badge"><span /> AI assistant</div>
      </header>
      <div className="conversation">
        {messages.length === 0 ? (
          <div className="welcome-state">
            <div className="welcome-icon"><Bot size={27} /></div>
            <h3>What would you like to know?</h3>
            <p>Ask a question about your PDF, or try a quick tool.</p>
            <div className="suggestions">
              <button onClick={() => onQuestionChange("What is this document about?")} disabled={disabled}>
                Summarize this document <CornerDownLeft size={14} />
              </button>
              <button onClick={() => onQuestionChange("What is 125 * 48?")} disabled={disabled}>
                Try the calculator <CornerDownLeft size={14} />
              </button>
              <button onClick={() => onQuestionChange("What is today's date?")} disabled={disabled}>
                Ask today's date <CornerDownLeft size={14} />
              </button>
            </div>
          </div>
        ) : (
          messages.map((message, index) => <Message key={index} message={message} />)
        )}
        {loading && (
          <div className="thinking"><span /><span /><span /> <em>Thinking...</em></div>
        )}
      </div>
      <form className="composer" onSubmit={onSend}>
        <input
          value={question}
          onChange={(event) => onQuestionChange(event.target.value)}
          placeholder="Ask about your document..."
          aria-label="Ask a question"
          disabled={loading}
        />
        <button className="primary-button send-button" type="submit" disabled={loading || !question.trim()}>
          <Send size={16} />
          <span>Send</span>
        </button>
      </form>
      <p className="composer-note">Answers are generated from your document and may need verification.</p>
    </section>
  );
}
