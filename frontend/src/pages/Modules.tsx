import { api } from '../api/client';
import { useAsync } from '../hooks/useAsync';

export function Modules({ openModule }: { openModule: (id: string) => void }) {
  const { data, loading, error } = useAsync(api.modules, []);
  if (loading) return <p>Loading modules...</p>;
  if (error || !data) return <p className="error">{error}</p>;
  return (
    <section>
      <h1>Modules</h1>
      <div className="module-grid">
        {data.map((module) => (
          <button key={module.id} className="module-card" onClick={() => openModule(module.id)}>
            <span>{String(module.order).padStart(2, '0')}</span>
            <h2>{module.title}</h2>
            <p>{module.description}</p>
            <small>{module.lesson_count} lessons · {module.question_count} questions · {module.challenge_count} challenge</small>
          </button>
        ))}
      </div>
    </section>
  );
}
