import { api } from '../api/client';
import { QuestionCard } from '../components/QuestionCard';
import { useAsync } from '../hooks/useAsync';

export function LessonPlayer({ lessonId, done }: { lessonId: string; done: () => void }) {
  const { data, loading, error } = useAsync(() => api.lesson(lessonId), [lessonId]);
  if (loading) return <p>Loading lesson...</p>;
  if (error || !data) return <p className="error">{error}</p>;
  const lesson = data.lesson;
  return (
    <section className="lesson">
      <p className="eyebrow">Learn mode</p>
      <h1>{lesson.title}</h1>
      <p className="lede">{lesson.summary}</p>
      <div className="panel">
        <p>{lesson.explanation}</p>
        <h2>Key points</h2>
        <ul>{lesson.key_points.map((point) => <li key={point}>{point}</li>)}</ul>
        <h2>Example</h2>
        {lesson.examples.map((example) => <pre key={example}>{example}</pre>)}
      </div>
      <h2>Check understanding</h2>
      {data.questions.map((question) => (
        <QuestionCard key={question.id} question={question} onSubmit={(answer) => api.attempt(data.module_id, question.id, answer, 0)} />
      ))}
      <button className="primary" onClick={async () => { await api.completeLesson(data.module_id, lesson.id); done(); }}>Mark lesson complete</button>
    </section>
  );
}
