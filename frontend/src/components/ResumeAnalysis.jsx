import { useState } from "react";

function ResumeAnalysis({ targetRole, setTargetRole }) {
  const [resume, setResume] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    if (!resume) {
      setError("Please select your resume PDF.");
      return;
    }

    setLoading(true);
    setError("");
    setResult("");

    const formData = new FormData();

    formData.append("target_role", targetRole);
    formData.append("resume", resume);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/resume-analysis",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Resume analysis failed");
      }

      const data = await response.json();

      setResult(data.result);
    } catch (error) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="feature-content">
      <h2>Resume Analysis</h2>

      <form onSubmit={handleSubmit}>
        <input
          className="form-input"
          placeholder="Target Role"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
        />

        <input
          className="form-input"
          type="file"
          accept=".pdf"
          onChange={(e) => setResume(e.target.files[0])}
        />

        <button
          className="primary-button"
          type="submit"
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>

        {loading && (
          <p className="status-message">
            Analyzing your resume...
          </p>
        )}

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}
      </form>

      {result && (
        <div className="result-box">
          <h2>Resume Analysis Result</h2>

          <p>{result}</p>
        </div>
      )}
    </div>
  );
}

export default ResumeAnalysis;