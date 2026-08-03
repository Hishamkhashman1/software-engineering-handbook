import { api } from '../api/client';
import { Stat } from '../components/Stat';
import { useAsync } from '../hooks/useAsync';

export function Dashboard({ openModule }: { openModule: (id: string) => void }) {
  const { data, loading, error } = useAsync(api.progress, []);
  if (loading) return <p>Loading dashboard...</p>;
  if (error || !data) return <p className="error">{error}</p>;
  const resume = data.module_progress.find((item) => item.completed_lessons < item.total_lessons);
  return (
    <section>
      <div className="hero">
        <div>
          <p className="eyebrow">Local interview preparation</p>
          <h1>Build mastery through lessons, quizzes, reviews, and code.</h1>
        </div>
        <button className="primary" onClick={() => resume && openModule(resume.module_id)} disabled={!resume}>Resume learning</button>
      </div>
      <div className="stats-grid">
        <Stat label="XP" value={data.total_xp} />
        <Stat label="Level" value={data.level} />
        <Stat label="Streak" value={data.current_streak} />
        <Stat label="Accuracy" value={`${Math.round(data.accuracy * 100)}%`} />
      </div>
      <div className="grid two">
        <div className="panel">
          <h2>Module Progress</h2>
          {data.module_progress.map((module) => (
            <button key={module.module_id} className="row-button" onClick={() => openModule(module.module_id)}>
              <span>{module.title}</span>
              <meter value={module.completed_lessons} max={module.total_lessons} />
            </button>
          ))}
        </div>
        <div className="panel">
          <h2>Weakest Topics</h2>
          {data.weakest_topics.length === 0 ? <p>No attempts yet.</p> : data.weakest_topics.map((topic) => (
            <div key={topic.topic} className="topic-row"><span>{topic.topic}</span><strong>{topic.mastery}</strong></div>
          ))}
          <h2>Recent Activity</h2>
          {data.recent_activity.map((item) => <p key={`${item.question_id}-${item.score}`}>{item.question_id}: {item.correct ? 'correct' : 'review'}</p>)}
        </div>
      </div>
    </section>
  );
}
