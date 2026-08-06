import { Check, X } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import type { GradeResult, Question } from '../types/content';
import { ConceptPanel } from './ConceptPanel';
import { shuffled } from '../utils/shuffle';

export function QuestionCard({
  question,
  onSubmit,
  feedbackMode = 'immediate'
}: {
  question: Question;
  onSubmit: (answer: unknown) => Promise<GradeResult | void>;
  feedbackMode?: 'immediate' | 'deferred';
}) {
  const orderingOptions = useMemo(() => shuffled(question.options ?? []), [question.id]);
  const [answer, setAnswer] = useState<unknown>(question.type === 'ordering' ? orderingOptions : '');
  const [feedback, setFeedback] = useState<GradeResult | null>(null);
  const [busy, setBusy] = useState(false);
  const options = useMemo(() => shuffled(question.options ?? []), [question.id]);
  const trueFalseOptions = useMemo(() => shuffled([true, false]), [question.id]);

  useEffect(() => {
    setAnswer(question.type === 'ordering' ? orderingOptions : '');
    setFeedback(null);
  }, [question.id, question.type, orderingOptions]);

  async function submit() {
    setBusy(true);
    const result = await onSubmit(answer);
    if (result && feedbackMode === 'immediate') setFeedback(result);
    setBusy(false);
  }

  return (
    <div className="question-card-layout">
      <article className="panel question-card">
        <div className="question-meta">
          <span>{question.type.replace('_', ' ')}</span>
          <span>Difficulty {question.difficulty}</span>
        </div>
        <h3>{question.prompt}</h3>
        {renderInput(question, answer, setAnswer, options, trueFalseOptions)}
        <button className="primary" onClick={submit} disabled={busy}>
          Submit
        </button>
        {feedback && (
          <div className={`feedback ${feedback.correct ? 'correct' : 'incorrect'}`}>
            {feedback.correct ? <Check size={18} /> : <X size={18} />}
            <div>
              <strong>{feedback.correct ? 'Correct' : `Score ${Math.round(feedback.score * 100)}%`}</strong>
              <p>{feedback.explanation}</p>
              {feedback.xp_awarded > 0 && <small>+{feedback.xp_awarded} XP</small>}
            </div>
          </div>
        )}
      </article>
      <ConceptPanel panel={question.concept_panel} />
    </div>
  );
}

function renderInput(question: Question, answer: unknown, setAnswer: (value: unknown) => void, options: string[], trueFalseOptions: boolean[]) {
  if (question.type === 'multiple_choice' || question.type === 'code_output') {
    return (
      <div className="options">
        {options.map((option) => (
          <label key={option} className={answer === option ? 'selected' : ''}>
            <input type="radio" name={question.id} checked={answer === option} onChange={() => setAnswer(option)} />
            {option}
          </label>
        ))}
      </div>
    );
  }
  if (question.type === 'true_false') {
    return (
      <div className="options two">
        {trueFalseOptions.map((option) => (
          <label key={String(option)} className={answer === option ? 'selected' : ''}>
            <input type="radio" name={question.id} checked={answer === option} onChange={() => setAnswer(option)} />
            {String(option)}
          </label>
        ))}
      </div>
    );
  }
  if (question.type === 'ordering') {
    const items = Array.isArray(answer) ? answer.map(String) : [];
    return (
      <div className="ordering">
        {items.map((item, index) => (
          <div key={item} className="order-row">
            <span>{item}</span>
            <button onClick={() => setAnswer(move(items, index, -1))} disabled={index === 0}>Up</button>
            <button onClick={() => setAnswer(move(items, index, 1))} disabled={index === items.length - 1}>Down</button>
          </div>
        ))}
      </div>
    );
  }
  return <textarea value={String(answer)} onChange={(event) => setAnswer(event.target.value)} rows={5} placeholder="Type a concise interview-style answer" />;
}

function move(items: string[], index: number, delta: number) {
  const copy = [...items];
  const next = index + delta;
  [copy[index], copy[next]] = [copy[next], copy[index]];
  return copy;
}
