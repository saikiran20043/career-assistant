import { useState } from "react";

function ResumeAnalysis({ targetRole, setTargetRole }) {
  const [resume, setResume] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    // Check whether a resume was selected
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
    <div>
      <h2>Resume Analysis</h2>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Target Role"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
        />

        <br />
        <br />

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setResume(e.target.files[0])}
        />

        <br />
        <br />

        <button type="submit">
          Analyze Resume
        </button>

        {loading && (
          <p>Analyzing your resume...</p>
        )}

        {error && (
          <p>{error}</p>
        )}
      </form>

      {result && (
        <>
          <hr />

          <h2>Resume Analysis Result</h2>

          <p>{result}</p>
        </>
      )}
    </div>
  );
}

export default ResumeAnalysis;