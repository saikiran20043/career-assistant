import { useState } from "react";

function SkillGap({ targetRole, setTargetRole }) {
  const [skills, setSkills] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/skill-gap",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            target_role: targetRole,
            skills: skills,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Skill gap analysis failed");
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
      <h2>Skill Gap Analysis</h2>

      <form onSubmit={handleSubmit}>

        <input
          className="form-input"
          placeholder="Target Role"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
        />

        <textarea
          className="form-input form-textarea"
          placeholder="Enter your current skills (e.g. Python, SQL, LangChain)"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
        />

        <button
          className="primary-button"
          type="submit"
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Skill Gap"}
        </button>

        {loading && (
          <p className="status-message">
            Analyzing your skills...
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
          <h2>Skill Gap Result</h2>

          <p>{result}</p>
        </div>
      )}
    </div>
  );
}

export default SkillGap;