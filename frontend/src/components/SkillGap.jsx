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
    <div>
      <h2>Skill Gap Analysis</h2>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Target Role"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
        />

        <br />
        <br />

        <textarea
          placeholder="Current Skills"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
        />

        <br />
        <br />

        <button type="submit">
          Analyze Skill Gap
        </button>

        {loading && (
          <p>Analyzing your skills...</p>
        )}

        {error && (
          <p>{error}</p>
        )}
      </form>

      {result && (
        <>
          <hr />

          <h2>Skill Gap Result</h2>

          <p>{result}</p>
        </>
      )}
    </div>
  );
}

export default SkillGap;