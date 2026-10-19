
import { useState } from "react";

const API_URL = "https://target-ai-ad-agent-latest.onrender.com";

export default function App() {
  const [url, setUrl] = useState("https://healthsportvoyageai.com");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function analyzeWebsite(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/analyze-site`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || `Request failed: HTTP ${response.status}`
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        `${err.message}. Проверь доступность API и попробуй ещё раз.`
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 px-5 py-10 text-slate-100">
      <div className="mx-auto max-w-5xl">
        <header className="mb-10">
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">
            Autonomous AI Marketing Agent
          </p>
          <h1 className="text-4xl font-bold tracking-tight md:text-6xl">
            Target AI Ad Agent
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-slate-400">
            Analyze a website, discover its audience, and generate
            targeted advertising content with AI.
          </p>
        </header>

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
          <h2 className="mb-2 text-xl font-semibold">Website analysis</h2>
          <p className="mb-5 text-sm text-slate-400">
            Enter a public website URL to start the five-step analysis.
          </p>

          <form onSubmit={analyzeWebsite} className="space-y-4">
            <label htmlFor="website-url" className="block text-sm font-medium">
              Website URL
            </label>
            <input
              id="website-url"
              type="url"
              required
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              placeholder="https://example.com"
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400"
            />

            <button
              type="submit"
              disabled={loading}
              className="rounded-xl bg-cyan-400 px-6 py-3 font-bold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Analyzing website..." : "Analyze website"}
            </button>
          </form>

          {loading && (
            <p className="mt-5 text-cyan-300" role="status">
              The AI agent is analyzing the website. The first request
              may take a little longer while the free server wakes up.
            </p>
          )}

          {error && (
            <div className="mt-6 rounded-xl border border-red-800 bg-red-950/40 p-4 text-red-200">
              <h3 className="font-semibold">Analysis failed</h3>
              <p className="mt-2 break-words">{error}</p>
            </div>
          )}
        </section>

        {result && (
          <section className="mt-8 space-y-6">
            <div className="rounded-2xl border border-emerald-800 bg-emerald-950/30 p-5">
              <p className="text-sm text-emerald-300">Analysis completed</p>
              <h2 className="mt-2 text-2xl font-bold">
                {result.title || "Marketing Analysis Report"}
              </h2>
              <p className="mt-2 text-slate-300">
                Steps completed: {result.steps_completed ?? "N/A"}
              </p>
            </div>

            {Array.isArray(result.step_results) &&
              result.step_results.map((step, index) => (
                <article
                  key={`${step.stage || "step"}-${index}`}
                  className="rounded-2xl border border-slate-800 bg-slate-900 p-6"
                >
                  <h3 className="mb-3 text-xl font-semibold text-cyan-300">
                    {step.stage || `Analysis step ${index + 1}`}
                  </h3>
                  <pre className="whitespace-pre-wrap break-words font-sans leading-7 text-slate-300">
                    {typeof step.result === "string"
                      ? step.result
                      : JSON.stringify(step.result, null, 2)}
                  </pre>
                </article>
              ))}

            {result.final_report && (
              <article className="rounded-2xl border border-cyan-800 bg-slate-900 p-6">
                <h2 className="mb-4 text-2xl font-bold">Final Marketing Report</h2>
                <pre className="whitespace-pre-wrap break-words font-sans leading-7 text-slate-200">
                  {result.final_report}
                </pre>
              </article>
            )}
          </section>
        )}

        <footer className="mt-12 border-t border-slate-800 pt-5 text-sm text-slate-500">
          Target AI Ad Agent · FastAPI · React · Vite · AI-powered marketing
        </footer>
      </div>
    </main>
  );
}
