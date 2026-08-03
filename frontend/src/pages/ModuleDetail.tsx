import { api } from '../api/client';
import { useAsync } from '../hooks/useAsync';

export function ModuleDetail({ moduleId, openLesson, openBoss }: { moduleId: string; openLesson: (id: string) => void; openBoss: (id: string) => void }) {
  const { data, loading, error } = useAsync(() => api.module(moduleId), [moduleId]);
  if (loading) return <p>Loading module...</p>;
  if (error || !data) return <p className="error">{error}</p>;
  return (
    <section>
      <p className="eyebrow">Module {data.order}</p>
      <h1>{data.title}</h1>
      <p className="lede">{data.description}</p>
      <div className="grid two">
        <div className="panel">
          <h2>Lessons</h2>
          {data.lessons.map((lesson) => (
            <button className="row-button" key={lesson.id} onClick={() => openLesson(lesson.id)}>
              <span>{lesson.title}</span>
              <small>Difficulty {lesson.difficulty}</small>
            </button>
          ))}
        </div>
        <div className="panel">
          <h2>Boss Battle</h2>
          <p>{data.boss_battle.title}</p>
          <p>Pass threshold: {Math.round(data.boss_battle.passing_threshold * 100)}%</p>
          <button className="primary" onClick={() => openBoss(data.id)}>Start boss battle</button>
        </div>
      </div>
    </section>
  );
}
