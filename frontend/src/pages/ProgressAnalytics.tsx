import { api } from '../api/client';
import { Stat } from '../components/Stat';
import { useAsync } from '../hooks/useAsync';

export function ProgressAnalytics() {
  const { data, loading, error } = useAsync(api.progress, []);
  if (loading) return <p>Loading analytics...</p>;
  if (error || !data) return <p className="error">{error}</p>;
  return (
    <section>
      <h1>Progress Analytics</h1>
      <div className="stats-grid">
        <Stat label="Best streak" value={data.best_streak} />
        <Stat label="Due reviews" value={data.due_reviews} />
        <Stat label="Avg response" value={`${data.average_response_time_ms}ms`} />
        <Stat label="Completed modules" value={data.completed_modules.length} />
      </div>
      <div className="panel">
        <h2>Topic Mastery</h2>
        {data.weakest_topics.map((topic) => (
          <div className="topic-row" key={topic.topic}>
            <span>{topic.topic}</span>
            <meter value={topic.mastery} max={100} />
          </div>
        ))}
      </div>
    </section>
  );
}
