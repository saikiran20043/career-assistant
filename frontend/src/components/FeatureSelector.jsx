function FeatureSelector({ selectedFeature, setSelectedFeature }) {
  return (
    <div className="feature-selector">

      <button
        className={selectedFeature === "skill-gap" ? "feature-button active" : "feature-button"}
        onClick={() => setSelectedFeature("skill-gap")}
      >
        Skill Gap
      </button>

      <button
        className={selectedFeature === "resume" ? "feature-button active" : "feature-button"}
        onClick={() => setSelectedFeature("resume")}
      >
        Resume Analysis
      </button>

      <button
        className={selectedFeature === "interview" ? "feature-button active" : "feature-button"}
        onClick={() => setSelectedFeature("interview")}
      >
        Interview Prep
      </button>

    </div>
  );
}

export default FeatureSelector;