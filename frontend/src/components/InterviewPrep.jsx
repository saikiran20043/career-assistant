import { useState } from "react";

function InterviewPrep({ targetRole, setTargetRole }) {
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    if (!targetRole.trim()) {
      setError("Please enter a target role.");
      return;
    }

    setLoading(true);
    setError("");
    setResult("");

    const formData = new FormData();

    formData.append("target_role", targetRole);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/interview-prep",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Interview preparation failed");
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
      <h2>Interview Preparation</h2>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Target Role"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
        />

        <br />
        <br />

        <button type="submit">
          Prepare Interview
        </button>

        {loading && (
          <p>Preparing your interview...</p>
        )}

        {error && (
          <p>{error}</p>
        )}
      </form>

      {result && (
        <>
          <hr />

          <h2>Interview Preparation Result</h2>

          <p>{result}</p>
        </>
      )}
    </div>
  );
}

export default InterviewPrep;