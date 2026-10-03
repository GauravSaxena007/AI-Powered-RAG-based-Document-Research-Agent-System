import { FileText, LoaderCircle, Upload } from "lucide-react";

export default function UploadPanel({
  file,
  documentName,
  uploading,
  onFileChange,
  onUpload,
}) {
  return (
    <section className="upload-card">
      <div className="section-heading">
        <div className="section-icon"><FileText size={19} /></div>
        <div>
          <h2>Your knowledge base</h2>
          <p>Upload a PDF to start a conversation</p>
        </div>
      </div>
      <div className="upload-controls">
        <label className="file-picker">
          <input type="file" accept="application/pdf,.pdf" onChange={onFileChange} />
          <FileText size={17} />
          <span>{file ? file.name : "Choose a PDF"}</span>
        </label>
        <button className="primary-button upload-button" onClick={onUpload} disabled={!file || uploading}>
          {uploading ? <LoaderCircle className="spin" size={17} /> : <Upload size={17} />}
          {uploading ? "Processing..." : "Upload"}
        </button>
      </div>
      {documentName ? (
        <div className="document-status">
          <span className="status-dot" />
          <span className="document-name">{documentName}</span>
          <span className="ready-label">Ready to chat</span>
        </div>
      ) : (
        <p className="upload-hint">PDF only · up to 25 MB</p>
      )}
    </section>
  );
}
