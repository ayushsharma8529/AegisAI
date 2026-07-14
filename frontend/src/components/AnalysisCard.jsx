function AnalysisCard({ analysis }) {
  if (!analysis) {
    return null;
  }

  return (
    <div className="rounded-2xl border border-gray-800 bg-gray-900 p-6 shadow-lg">

      <h2 className="mb-6 text-2xl font-bold text-cyan-400">
        🤖 AI Security Analysis
      </h2>

      <div className="rounded-xl bg-gray-800 p-5">

        <pre className="whitespace-pre-wrap break-words text-gray-200 leading-7 font-sans">
          {analysis}
        </pre>

      </div>

    </div>
  );
}

export default AnalysisCard;