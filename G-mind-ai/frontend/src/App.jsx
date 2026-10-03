import { useState } from "react";
import { BrainCircuit, Sparkles } from "lucide-react";
import ChatPanel from "./components/ChatPanel";
import UploadPanel from "./components/UploadPanel";

async function readApiResponse(response, fallbackMessage) {
  const responseText = await response.text();
  let data;

  try {
    data = responseText ? JSON.parse(responseText) : {};
  } catch {
    if (!response.ok) {
      throw new Error(
        response.status >= 500
          ? `Server error (${response.status}). Check the backend terminal for details.`
          : responseText || fallbackMessage,
      );
    }
    throw new Error("The server returned an invalid response. Please try again.");
  }

  if (!response.ok) {
    throw new Error(data.detail || `${fallbackMessage} (HTTP ${response.status})`);
  }
  return data;
}

export default function App() {
  const [file, setFile] = useState(null);
  const [document, setDocument] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [messages, setMessages] = useState([]);

  async function uploadDocument() {
    if (!file) return;
    setUploading(true);
    setError("");
    setMessages([]);
    const form = new FormData();
    form.append("file", file);
    try {
      const response = await fetch("/api/documents/upload", { method: "POST", body: form });
      const data = await readApiResponse(response, "Could not process this PDF.");
      setDocument(data);
      setFile(null);
    } catch (uploadError) {
      setError(uploadError.message);
    } finally {
      setUploading(false);
    }
  }

  async function sendQuestion(event) {
    event.preventDefault();
    const text = question.trim();
    if (!text || loading) return;
    setQuestion("");
    setError("");
    setMessages((current) => [...current, { role: "user", content: text }]);
    setLoading(true);
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text, document_id: document?.document_id }),
      });
      const data = await readApiResponse(response, "The assistant could not answer.");
      setMessages((current) => [...current, { role: "assistant", content: data.answer, sources: data.sources }]);
    } catch (chatError) {
      setError(chatError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page-shell">
      <nav className="topbar">
        <a className="brand" href="/" aria-label="DocMind AI home">
          <span className="brand-mark"><BrainCircuit size={21} /></span>
          <span>G-Mind <b>AI</b></span>
        </a>
        <div className="topbar-right"><span className="online-dot" /> Your private research workspace</div>
      </nav>
      <div className="main-content">
        <header className="hero">
          <div className="hero-copy">
            <div className="hero-kicker"><Sparkles size={14} /> YOUR DOCUMENT, UNDERSTOOD</div>
            <h1>Research at the speed<br />of <span>thought.</span></h1>
            <p>Upload a document. Ask anything. Get answers grounded in your sources.</p>
          </div>
          <div className="hero-art" aria-hidden="true">
            <div className="art-orbit orbit-one" /><div className="art-orbit orbit-two" />
            <div className="art-center"><BrainCircuit size={42} /></div>
            <span className="art-spark spark-one">✦</span><span className="art-spark spark-two">✧</span>
          </div>
        </header>
        <div className="workspace">
          <UploadPanel
            file={file}
            documentName={document?.filename}
            uploading={uploading}
            onFileChange={(event) => setFile(event.target.files?.[0] || null)}
            onUpload={uploadDocument}
          />
          <ChatPanel
            messages={messages}
            question={question}
            loading={loading}
            disabled={!document}
            onQuestionChange={setQuestion}
            onSend={sendQuestion}
          />
          {error && <div className="error-banner" role="alert">{error}</div>}
        </div>
        <footer className="footer">Built by Gaurav <span>·</span> Powered by AI</footer>
      </div>
    </main>
  );
}
