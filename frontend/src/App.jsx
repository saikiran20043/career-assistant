import { useState } from "react";

import Header from "./components/Header";
import FeatureSelector from "./components/FeatureSelector";
import SkillGap from "./components/SkillGap";
import ResumeAnalysis from "./components/ResumeAnalysis";
import InterviewPrep from "./components/InterviewPrep";


function App() {
  const [targetRole, setTargetRole] = useState("");
  const [selectedFeature, setSelectedFeature] = useState("skill-gap");


  return (
    <div style={{ padding: "30px", maxWidth: "700px" }}>

      <Header />

      <FeatureSelector
        selectedFeature={selectedFeature}
        setSelectedFeature={setSelectedFeature}
      />


      {selectedFeature === "skill-gap" && (
        <SkillGap
          targetRole={targetRole}
          setTargetRole={setTargetRole}
        />
      )}


      {selectedFeature === "resume" && (
        <ResumeAnalysis
          targetRole={targetRole}
          setTargetRole={setTargetRole}
        />
      )}


      {selectedFeature === "interview" && (
        <InterviewPrep
          targetRole={targetRole}
          setTargetRole={setTargetRole}
        />
      )}

    </div>
  );
}


export default App;