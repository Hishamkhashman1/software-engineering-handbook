import { useState } from 'react';
import { api } from '../api/client';
import { QuestionCard } from '../components/QuestionCard';
import { useAsync } from '../hooks/useAsync';
import type { Question } from '../types/content';

export function QuizPlayer({ mode = 'quiz', bossModuleId }: { mode?: 'quiz' | 'review' | 'boss'; bossModuleId?: string }) {
  const [count, setCount] = useState(10);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [score, setScore] = useState<{ correct: number; total: number } | null>(null);
  const [answers, setAnswers] = useState<Record<string, unknown>>({});
  const [bossResult, setBossResult] = useState<string | null>(null);
  const modules = useAsync(api.modules, []);

  async function start() {
    if (mode === 'review') {
      setQuestions((await api.weak()).questions);
    } else if (mode === 'boss' && bossModuleId) {
      const module = await api.module(bossModuleId);
      setQuestions(module.questions.filter((question) => module.boss_battle.question_ids.includes(question.id)));
    } else {
      setQuestions((await api.quiz([], count)).questions);
    }
    setScore({ correct: 0, total: 0 });
    setAnswers({});
    setBossResult(null);
  }

  async function finishBoss() {
    if (!bossModuleId) return;
    const result = await api.submitBoss(bossModuleId, questions.map((question) => ({
      module_id: bossModuleId,
      question_id: question.id,
      answer: answers[question.id],
      response_time_ms: 0
    })));
    setBossResult(`${result.passed ? 'Badge awarded' : 'Review recommended'} · ${Math.round(result.score * 100)}%`);
  }

  return (
    <section>
      <h1>{mode === 'review' ? 'Weak Topics Review' : mode === 'boss' ? 'Boss Battle' : 'Quick Quiz'}</h1>
      {questions.length === 0 && (
        <div className="panel controls">
          {mode === 'quiz' && <label>Question count <input type="number" min={5} max={30} value={count} onChange={(event) => setCount(Number(event.target.value))} /></label>}
          {modules.data && mode === 'quiz' && <p>{modules.data.length} modules available for mixed practice.</p>}
          <button className="primary" onClick={start}>Start</button>
        </div>
      )}
      {score && <p className="score">Answered {score.total}; correct {score.correct}</p>}
      {questions.map((question) => (
        <QuestionCard key={question.id} question={question} onSubmit={async (answer) => {
          const moduleId = question.id.split('-q')[0];
          setAnswers((prev) => ({ ...prev, [question.id]: answer }));
          const result = await api.attempt(moduleId, question.id, answer, 0);
          setScore((prev) => prev ? { correct: prev.correct + (result.correct ? 1 : 0), total: prev.total + 1 } : prev);
          return result;
        }} />
      ))}
      {mode === 'boss' && questions.length > 0 && <button className="primary" onClick={finishBoss}>Finish boss battle</button>}
      {bossResult && <div className="panel feedback correct"><strong>{bossResult}</strong></div>}
    </section>
  );
}
