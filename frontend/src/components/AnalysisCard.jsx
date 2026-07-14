function AnalysisCard({ analysis }) {
  if (!analysis) {
    return null;
  }

  return (
    <div>
      <h2>AI Security Analysis</h2>

      <pre>{analysis}</pre>
    </div>
  );
}

export default AnalysisCard;