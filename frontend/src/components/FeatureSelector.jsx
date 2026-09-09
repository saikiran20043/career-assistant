function FeatureSelector({ selectedFeature, setSelectedFeature }) {
  return (
    <div>
      <button
        onClick={() => setSelectedFeature("skill-gap")}
      >
        Skill Gap
      </button>

      <button
        onClick={() => setSelectedFeature("resume")}
      >
        Resume Analysis
      </button>

      <button
        onClick={() => setSelectedFeature("interview")}
      >
        Interview Prep
      </button>

      <p>Selected: {selectedFeature}</p>
    </div>
  );
}

export default FeatureSelector;