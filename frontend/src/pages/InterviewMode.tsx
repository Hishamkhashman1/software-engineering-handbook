import { useState } from 'react';
import { api } from '../api/client';
import { QuestionCard } from '../components/QuestionCard';
import type { Question } from '../types/content';

export function InterviewMode() {
  const [session, setSession] = useState<{ id: string; duration: number; questions: Question[] } | null>(null);
  const [answers, setAnswers] = useState<Record<string, unknown>>({});
  const [result, setResult] = useState<string | null>(null);

  async function start() {
    const created = await api.interview(15);
    setSession({ id: created.session_id, duration: created.duration_seconds, questions: created.questions });
    setAnswers({});
    setResult(null);
  }

  async function submit() {
    if (!session) return;
    const payload = session.questions.map((question) => ({
      module_id: question.id.split('-q')[0],
      question_id: question.id,
      answer: answers[question.id],
      response_time_ms: 0
    }));
    const response = await api.submitInterview(session.id, payload);
    setResult(`Final score ${Math.round(response.score * 100)}%`);
  }

  return (
    <section>
      <h1>Interview Mode</h1>
      {!session && <div className="panel"><p>Timed mixed practice with feedback withheld until submission.</p><button className="primary" onClick={start}>Start 15-question interview</button></div>}
      {session && <p className="score">Time box: {Math.round(session.duration / 60)} minutes</p>}
      {session?.questions.map((question) => (
        <QuestionCard key={question.id} question={question} feedbackMode="deferred" onSubmit={async (answer) => {
          setAnswers((prev) => ({ ...prev, [question.id]: answer }));
        }} />
      ))}
      {session && <button className="primary" onClick={submit}>Submit interview</button>}
      {result && <div className="panel feedback correct"><strong>{result}</strong></div>}
    </section>
  );
}
