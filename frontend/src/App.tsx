import { CheckCircle2, ChevronRight, Code2, Lock, Settings, Swords, Trophy } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import type { KeyboardEvent } from 'react';
import { api } from './api/client';
import { ConceptPanel } from './components/ConceptPanel';
import type { CodingChallenge, GradeResult, ModuleDetail, ModuleSummary, Progress, Question } from './types/content';

export function App() {
  const [view, setView] = useState<View>('home');
  const [modules, setModules] = useState<ModuleSummary[]>([]);
  const [progress, setProgress] = useState<Progress | null>(null);
  const [activeModule, setActiveModule] = useState<string | null>(null);
  const [soundEnabled, setSoundEnabled] = useState(() => localStorage.getItem('sound') !== 'off');

  async function refresh() {
    const [moduleData, progressData] = await Promise.all([api.modules(), api.progress()]);
    setModules(moduleData);
    setProgress(progressData);
  }

  useEffect(() => { refresh(); }, []);
  useEffect(() => {
    if (view === 'home') setActiveModule(null);
  }, [view]);

  function play(kind: SoundKind) {
    if (!soundEnabled) return;
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return;
    const ctx = new AudioContextClass();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.frequency.value = kind === 'correct' ? 660 : kind === 'wrong' ? 170 : kind === 'boss' ? 95 : 880;
    gain.gain.value = 0.025;
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.09);
  }

  return (
    <div className="game-shell">
      <TopBar progress={progress} view={view} setView={setView} />
      {view === 'home' && <Home modules={modules} progress={progress} setView={setView} startModule={(id) => { setActiveModule(id); setView('run'); }} />}
      {view === 'roadmap' && <Roadmap modules={modules} progress={progress} startModule={(id) => { setActiveModule(id); setView('run'); }} startBoss={(id) => { setActiveModule(id); setView('boss'); }} />}
      {view === 'run' && <ChallengeRun kind={activeModule ? 'module' : 'daily'} moduleId={activeModule} onDone={async () => { setActiveModule(null); await refresh(); setView('home'); }} play={play} />}
      {view === 'weak' && <ChallengeRun kind="weak" moduleId={null} onDone={async () => { await refresh(); setView('home'); }} play={play} />}
      {view === 'boss' && activeModule && <BossBattle moduleId={activeModule} onDone={async () => { await refresh(); setView('home'); }} play={play} />}
      {view === 'coding' && <CodingBattle modules={modules.filter((module) => isUnlocked(module, progress))} progress={progress} play={play} refreshProgress={refresh} />}
      {view === 'settings' && <SettingsStage soundEnabled={soundEnabled} setSoundEnabled={setSoundEnabled} />}
    </div>
  );
}

type View = 'home' | 'run' | 'weak' | 'roadmap' | 'boss' | 'coding' | 'settings';
type RunKind = 'daily' | 'weak' | 'module';
type SoundKind = 'correct' | 'wrong' | 'level' | 'boss';
type Feedback = GradeResult & { answer: unknown };

const ranks = ['Intern', 'Junior', 'Mid-Level', 'Senior', 'Principal', 'Staff', 'Distinguished Engineer'];

function rankForLevel(level: number) {
  return ranks[Math.min(ranks.length - 1, Math.floor((level - 1) / 3))];
}

function xpIntoLevel(totalXp: number) {
  let remaining = totalXp;
  let threshold = 100;
  while (remaining >= threshold) {
    remaining -= threshold;
    threshold += 50;
  }
  return { current: remaining, threshold };
}

function isUnlocked(module: ModuleSummary, progress: Progress | null) {
  void module;
  void progress;
  return true;
}

function TopBar({ progress, view, setView }: { progress: Progress | null; view: View; setView: (view: View) => void }) {
  const xp = xpIntoLevel(progress?.total_xp ?? 0);
  return (
    <header className="topbar">
      <button className="wordmark" onClick={() => setView('home')}>Interview Game</button>
      <div className="rank-strip">
        <strong>{rankForLevel(progress?.level ?? 1)} Engineer Lv. {progress?.level ?? 1}</strong>
        <div className="xp-track"><span style={{ width: `${Math.round((xp.current / xp.threshold) * 100)}%` }} /></div>
      </div>
      <nav className="quick-nav">
        <button className={view === 'roadmap' ? 'active' : ''} onClick={() => setView('roadmap')}>Roadmap</button>
        <button className={view === 'coding' ? 'active' : ''} onClick={() => setView('coding')}>Code</button>
        <button className={view === 'settings' ? 'active icon-only' : 'icon-only'} aria-label="Settings" onClick={() => setView('settings')}><Settings size={18} /></button>
      </nav>
    </header>
  );
}

function Home({ modules, progress, setView, startModule }: { modules: ModuleSummary[]; progress: Progress | null; setView: (view: View) => void; startModule: (id: string) => void }) {
  const weakest = progress?.weakest_topics[0];
  const next = modules.find((module) => isUnlocked(module, progress) && !progress?.completed_modules.includes(module.id)) ?? modules[0];
  return (
    <main className="home-stage">
      <section className="daily-card">
        <div>
          <p className="kicker">Today's Run</p>
          <h1>8 minutes. One clean streak.</h1>
          <p>Short challenge chain. Immediate feedback. No menus between reps.</p>
        </div>
        <button className="action-button" onClick={() => setView('run')}>Start run <ChevronRight size={24} /></button>
      </section>
      <section className="focus-grid">
        <button className="focus-card streak-card" onClick={() => setView('run')}>
          <span>Knowledge Streak</span>
          <strong>{progress?.current_streak ?? 0} Days</strong>
          <small>Do not break it.</small>
        </button>
        <button className="focus-card danger-card" onClick={() => setView('weak')}>
          <span>Weakest Skill</span>
          <strong>{weakest?.topic ?? 'Unseen topics'}</strong>
          <small>Interview success {weakest ? Math.max(35, Math.round(100 - weakest.mastery / 2)) : 50}%</small>
        </button>
        <button className="focus-card" onClick={() => next && startModule(next.id)}>
          <span>Next Unlock</span>
          <strong>{next?.title ?? 'Roadmap clear'}</strong>
          <small>One more challenge opens the path.</small>
        </button>
      </section>
    </main>
  );
}

function Roadmap({ modules, progress, startModule, startBoss }: { modules: ModuleSummary[]; progress: Progress | null; startModule: (id: string) => void; startBoss: (id: string) => void }) {
  return (
    <main className="roadmap">
      <p className="kicker">Roadmap</p>
      <h1>{rankForLevel(progress?.level ?? 1)} track</h1>
      <div className="module-path">
        {modules.map((module) => {
          const unlocked = isUnlocked(module, progress);
          const moduleProgress = progress?.module_progress.find((item) => item.module_id === module.id);
          const trainingPercent = moduleProgress?.training_percent ?? 0;
          const bossComplete = moduleProgress?.boss_completed ?? progress?.completed_modules.includes(module.id) ?? false;
          const complete = bossComplete;
          return (
            <article key={module.id} className={`path-node ${unlocked ? '' : 'locked'} ${complete ? 'complete' : ''}`}>
              <span className="node-index">{complete ? <Trophy size={18} /> : unlocked ? module.order : <Lock size={18} />}</span>
              <div>
                <h2>{module.title}</h2>
                <p>{unlocked ? module.description : unlockCopy(module)}</p>
                <div className="node-progress" aria-label={`${module.title} progress`}>
                  <div>
                    <span>Training</span>
                    <strong>{trainingPercent}%</strong>
                  </div>
                  <div className="mini-track"><span style={{ width: `${trainingPercent}%` }} /></div>
                  <div className={bossComplete ? 'status-pill done' : 'status-pill'}>
                    {bossComplete ? <CheckCircle2 size={14} /> : <Swords size={14} />}
                    {bossComplete ? 'Boss cleared' : 'Boss open'}
                  </div>
                </div>
              </div>
              <div className="node-actions">
                <button disabled={!unlocked} onClick={() => startModule(module.id)}>{trainingPercent > 0 ? 'Continue' : 'Train'}</button>
                <button className={bossComplete ? 'cleared' : ''} disabled={!unlocked} onClick={() => startBoss(module.id)}><Swords size={16} /> {bossComplete ? 'Replay' : 'Boss'}</button>
              </div>
            </article>
          );
        })}
      </div>
    </main>
  );
}

function ChallengeRun({ kind, moduleId, onDone, play }: { kind: RunKind; moduleId: string | null; onDone: () => void; play: (kind: SoundKind) => void }) {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [index, setIndex] = useState(0);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [combo, setCombo] = useState(0);
  const [bestCombo, setBestCombo] = useState(0);
  const [runXp, setRunXp] = useState(0);
  const [phase, setPhase] = useState<'loading' | 'answer' | 'feedback' | 'done'>('loading');
  const [flash, setFlash] = useState<'correct' | 'wrong' | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      const data = kind === 'weak' ? await api.weak() : await api.quiz(moduleId ? [moduleId] : [], kind === 'daily' ? 6 : 8);
      setQuestions(data.questions);
      setPhase('answer');
    }
    load();
  }, [kind, moduleId]);

  const question = questions[index];

  async function answer(value: unknown) {
    if (!question || phase !== 'answer' || isSubmitting) return;
    setIsSubmitting(true);
    setSubmitError(null);
    try {
      const result = await api.attempt(question.id.split('-q')[0], question.id, value, 0);
      const nextCombo = result.correct ? combo + 1 : 0;
      const comboBonus = result.correct ? Math.floor(result.xp_awarded * Math.min(1.5, nextCombo * 0.12)) : 0;
      setCombo(nextCombo);
      setBestCombo((current) => Math.max(current, nextCombo));
      setRunXp((xp) => xp + result.xp_awarded + comboBonus);
      setFeedback({ ...result, xp_awarded: result.xp_awarded + comboBonus, answer: value });
      setFlash(result.correct ? 'correct' : 'wrong');
      play(result.correct ? 'correct' : 'wrong');
      setPhase('feedback');
      window.setTimeout(() => setFlash(null), 520);
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Could not submit answer. Check that the backend is running.');
    } finally {
      setIsSubmitting(false);
    }
  }

  function next() {
    if (index + 1 >= questions.length) {
      setPhase('done');
      return;
    }
    setIndex(index + 1);
    setFeedback(null);
    setSubmitError(null);
    setPhase('answer');
  }

  if (phase === 'loading') return <main className="challenge-stage"><section className="challenge-card">Loading challenge...</section></main>;
  if (phase === 'done') return <main className="challenge-stage"><section className="finish-card"><p className="kicker">Run complete</p><h1>+{runXp} XP</h1><p>Best combo x{Math.max(1, bestCombo)}. The next challenge is already ready.</p><button className="action-button" onClick={onDone}>Claim and continue</button></section></main>;

  return (
    <main className={`challenge-stage ${flash ?? ''}`}>
      <RunHud label={kind === 'weak' ? 'Weak skill drill' : kind === 'daily' ? "Today's run" : 'Module duel'} index={index + 1} total={questions.length} combo={combo} runXp={runXp} />
      {question && <OneQuestion key={question.id} question={question} feedback={feedback} submitError={submitError} isSubmitting={isSubmitting} onAnswer={answer} onNext={next} />}
    </main>
  );
}

function OneQuestion({ question, feedback, submitError, isSubmitting, onAnswer, onNext, nextLabel = 'Next challenge' }: { question: Question; feedback: Feedback | null; submitError: string | null; isSubmitting: boolean; onAnswer: (value: unknown) => void; onNext: () => void; nextLabel?: string }) {
  const locked = feedback !== null || isSubmitting;
  return (
    <section className={`challenge-layout ${feedback ? (feedback.correct ? 'is-correct' : 'is-wrong') : ''}`}>
      <div className="challenge-card">
        <div className="question-kind">{question.type.replace('_', ' ')} · Difficulty {question.difficulty}</div>
        {question.code && <pre className="snippet">{question.code}</pre>}
        <h1>{question.prompt}</h1>
        {question.type === 'multi_select' ? (
          <MultiSelectAnswer question={question} disabled={locked} submit={onAnswer} />
        ) : question.type === 'matching' ? (
          <MatchingAnswer question={question} disabled={locked} submit={onAnswer} />
        ) : question.type === 'code_fill' ? (
          <CodeFillAnswer question={question} disabled={locked} submit={onAnswer} />
        ) : question.options && question.type !== 'ordering' ? (
          <div className="answer-grid">
            {question.options.map((option) => <button key={option} disabled={locked} onClick={() => onAnswer(option)}>{option}</button>)}
          </div>
        ) : question.type === 'true_false' ? (
          <div className="answer-grid two"><button disabled={locked} onClick={() => onAnswer(true)}>True</button><button disabled={locked} onClick={() => onAnswer(false)}>False</button></div>
        ) : question.type === 'ordering' ? (
          <OrderingAnswer question={question} disabled={locked} submit={onAnswer} />
        ) : (
          <div className="answer-grid"><button disabled={locked} onClick={() => onAnswer('__ack__')}>Reveal the pattern</button></div>
        )}
        {submitError && <div className="submit-error" role="alert">{submitError}</div>}
        {feedback && (
          <div className="result-panel">
            <div className="result-mark">{feedback.correct ? 'Locked in' : 'Pattern revealed'}</div>
            <div className="xp-pop">+{Math.max(4, feedback.xp_awarded)} XP</div>
            {!feedback.correct && <AnswerReveal selected={feedback.answer} expected={feedback.expected} />}
            <div className="reason-block">
              <span>{feedback.correct ? 'Why this is right' : 'Why that answer wins'}</span>
              <p>{feedback.explanation}</p>
            </div>
            <button className="action-button" onClick={onNext}>{nextLabel} <ChevronRight size={22} /></button>
          </div>
        )}
      </div>
      <ConceptPanel panel={question.concept_panel} />
    </section>
  );
}

function AnswerReveal({ selected, expected }: { selected: unknown; expected: unknown }) {
  return (
    <div className="answer-reveal">
      <div>
        <span>Your answer</span>
        <strong>{formatAnswer(selected)}</strong>
      </div>
      <div>
        <span>Correct answer</span>
        <strong>{formatAnswer(expected)}</strong>
      </div>
    </div>
  );
}

function formatAnswer(value: unknown): string {
  if (Array.isArray(value)) return value.join(', ');
  if (value && typeof value === 'object') {
    return Object.entries(value as Record<string, unknown>).map(([key, item]) => `${key} -> ${String(item)}`).join(' · ');
  }
  if (typeof value === 'boolean') return value ? 'True' : 'False';
  if (value === null || value === undefined || value === '') return 'No answer';
  return String(value);
}

function MultiSelectAnswer({ question, disabled, submit }: { question: Question; disabled: boolean; submit: (value: unknown) => void }) {
  const [selected, setSelected] = useState<string[]>([]);
  function toggle(option: string) {
    setSelected((current) => current.includes(option) ? current.filter((item) => item !== option) : [...current, option]);
  }
  return (
    <div className="answer-grid">
      {(question.options ?? []).map((option) => (
        <button key={option} className={selected.includes(option) ? 'picked' : ''} disabled={disabled} onClick={() => toggle(option)}>{option}</button>
      ))}
      <button className="lock-wide" disabled={disabled || selected.length === 0} onClick={() => submit(selected)}>Lock selection</button>
    </div>
  );
}

function MatchingAnswer({ question, disabled, submit }: { question: Question; disabled: boolean; submit: (value: unknown) => void }) {
  const pairs = question.pairs ?? [];
  const choices = [...pairs.map((pair) => pair.right)].sort();
  const [answers, setAnswers] = useState<Record<string, string>>({});
  return (
    <div className="match-stack">
      {pairs.map((pair) => (
        <label key={pair.left}>
          <span>{pair.left}</span>
          <select disabled={disabled} value={answers[pair.left] ?? ''} onChange={(event) => setAnswers((current) => ({ ...current, [pair.left]: event.target.value }))}>
            <option value="">Match...</option>
            {choices.map((choice) => <option key={choice} value={choice}>{choice}</option>)}
          </select>
        </label>
      ))}
      <button disabled={disabled || Object.keys(answers).length !== pairs.length} onClick={() => submit(answers)}>Lock matches</button>
    </div>
  );
}

function CodeFillAnswer({ question, disabled, submit }: { question: Question; disabled: boolean; submit: (value: unknown) => void }) {
  return (
    <div className="answer-grid">
      {(question.options ?? []).map((option) => <button key={option} disabled={disabled} onClick={() => submit(option)}><code>{option}</code></button>)}
    </div>
  );
}

function OrderingAnswer({ question, disabled, submit }: { question: Question; disabled: boolean; submit: (value: unknown) => void }) {
  const [items, setItems] = useState(() => [...(question.options ?? [])]);
  function move(index: number, delta: number) {
    const next = index + delta;
    const copy = [...items];
    [copy[index], copy[next]] = [copy[next], copy[index]];
    setItems(copy);
  }
  return (
    <div className="order-stack">
      {items.map((item, index) => (
        <div key={item}>
          <span>{item}</span>
          <button disabled={disabled || index === 0} onClick={() => move(index, -1)}>Up</button>
          <button disabled={disabled || index === items.length - 1} onClick={() => move(index, 1)}>Down</button>
        </div>
      ))}
      <button disabled={disabled} onClick={() => submit(items)}>Lock order</button>
    </div>
  );
}

function RunHud({ label, index, total, combo, runXp }: { label: string; index: number; total: number; combo: number; runXp: number }) {
  return (
    <div className="run-hud">
      <span>{label}</span>
      <div className="mini-track"><span style={{ width: `${(index / total) * 100}%` }} /></div>
      <strong>Combo x{Math.max(1, combo)}</strong>
      <strong>+{runXp} XP</strong>
    </div>
  );
}

function BossBattle({ moduleId, onDone, play }: { moduleId: string; onDone: () => void; play: (kind: SoundKind) => void }) {
  const [module, setModule] = useState<ModuleDetail | null>(null);
  const [index, setIndex] = useState(0);
  const [bossHp, setBossHp] = useState(100);
  const [playerHp, setPlayerHp] = useState(100);
  const [answers, setAnswers] = useState<Record<string, unknown>>({});
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [done, setDone] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => { api.module(moduleId).then(setModule); }, [moduleId]);
  const questions = useMemo(() => module ? module.questions.filter((q) => module.boss_battle.question_ids.includes(q.id)) : [], [module]);
  const question = questions[index];
  const battleEnding = bossHp <= 0 || playerHp <= 0 || index + 1 >= questions.length;

  async function answer(value: unknown) {
    if (!question || feedback || isSubmitting) return;
    setIsSubmitting(true);
    setSubmitError(null);
    try {
      const result = await api.attempt(moduleId, question.id, value, 0);
      setAnswers((prev) => ({ ...prev, [question.id]: value }));
      setFeedback({ ...result, answer: value });
      if (result.correct) {
        setBossHp((hp) => Math.max(0, hp - 18));
        play('boss');
      } else {
        setPlayerHp((hp) => Math.max(0, hp - 22));
        play('wrong');
      }
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Could not submit answer. Check that the backend is running.');
    } finally {
      setIsSubmitting(false);
    }
  }

  async function next() {
    if (bossHp <= 0 || playerHp <= 0 || index + 1 >= questions.length) {
      const payload = Object.entries(answers).map(([questionId, answer]) => ({ module_id: moduleId, question_id: questionId, answer, response_time_ms: 0 }));
      const result = await api.submitBoss(moduleId, payload);
      setDone(result.passed ? `Boss defeated. Badge unlocked. ${Math.round(result.score * 100)}%.` : `Battle lost. ${Math.round(result.score * 100)}%. Train one weak skill and return.`);
      return;
    }
    setIndex(index + 1);
    setFeedback(null);
    setSubmitError(null);
  }

  if (!module || !question) return <main className="challenge-stage"><section className="challenge-card">Loading boss...</section></main>;
  if (done) return <main className="challenge-stage"><section className="finish-card"><p className="kicker">Boss Battle</p><h1>{done}</h1><button className="action-button" onClick={onDone}>Return home</button></section></main>;
  return (
    <main className="boss-stage">
      <div className="boss-board">
        <Combatant title="Senior Backend Engineer" hp={bossHp} />
        <Combatant title="You" hp={playerHp} />
      </div>
      <OneQuestion question={question} feedback={feedback} submitError={submitError} isSubmitting={isSubmitting} onAnswer={answer} onNext={next} nextLabel={battleEnding ? 'Finish battle' : 'Next challenge'} />
    </main>
  );
}

function Combatant({ title, hp }: { title: string; hp: number }) {
  return <div className="combatant"><span>{title}</span><div className="hp"><span style={{ width: `${hp}%` }} /></div><strong>{hp} HP</strong></div>;
}

function CodingBattle({ modules, progress, play, refreshProgress }: { modules: ModuleSummary[]; progress: Progress | null; play: (kind: SoundKind) => void; refreshProgress: () => Promise<void> }) {
  const [moduleId, setModuleId] = useState(modules[0]?.id ?? '');
  const [detail, setDetail] = useState<ModuleDetail | null>(null);
  const [code, setCode] = useState('');
  const [result, setResult] = useState<{ passed: boolean; tests: unknown[]; stderr?: string; error?: string; timeout?: boolean } | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [runError, setRunError] = useState<string | null>(null);

  useEffect(() => {
    if (modules.length > 0 && !moduleId) setModuleId(modules[0].id);
  }, [modules, moduleId]);

  useEffect(() => {
    if (!moduleId) return;
    api.module(moduleId).then((data) => {
      const nextChallenge = data.coding_challenges[0];
      const saved = progress?.coding_progress.find((item) => item.module_id === data.id && item.challenge_id === nextChallenge?.id);
      setDetail(data);
      setCode(saved?.code ?? nextChallenge?.starter_code ?? '');
      setResult(saved?.result ?? null);
      setRunError(null);
    });
  }, [moduleId, progress]);

  const challenge: CodingChallenge | undefined = detail?.coding_challenges[0];
  const solved = result?.passed ?? false;

  async function runTests() {
    if (!challenge || isRunning) return;
    setIsRunning(true);
    setRunError(null);
    try {
      const output = await api.runCode(moduleId, challenge.id, code);
      setResult(output);
      play(output.passed ? 'correct' : 'wrong');
      await refreshProgress();
    } catch (error) {
      setRunError(error instanceof Error ? error.message : 'Could not run tests. Check that the backend is running.');
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <main className="coding-stage">
      <div className="mission-bar">
        <strong>Bug Report</strong>
        <select value={moduleId} onChange={(event) => setModuleId(event.target.value)}>
          {modules.map((module) => <option key={module.id} value={module.id}>{module.title}</option>)}
        </select>
      </div>
      {challenge && (
        <section className="code-mission">
          <aside>
            <p className="kicker">Production API is failing</p>
            <h1>{challenge.title}</h1>
            <p>{challenge.instructions}</p>
            <div className="test-list">{challenge.visible_tests.map((test) => <span key={test.name} className={solved ? 'passed' : ''}>{solved ? 'Passing' : 'Failing'}: {test.name}</span>)}</div>
          </aside>
          <div className="editor-card">
            <textarea value={code} onChange={(event) => setCode(event.target.value)} onKeyDown={(event) => handleCodeEditorKeyDown(event, setCode)} spellCheck={false} />
            <button className="action-button" onClick={runTests} disabled={isRunning}>{isRunning ? 'Running...' : solved ? 'Run again' : 'Run tests'} <Code2 size={20} /></button>
            {runError && <div className="submit-error" role="alert">{runError}</div>}
          </div>
          {result && <div className={`test-result ${result.passed ? 'passed' : 'failed'}`}><strong>{result.passed ? 'All tests green' : 'Still failing'}</strong><pre>{JSON.stringify(result, null, 2)}</pre></div>}
        </section>
      )}
    </main>
  );
}

function handleCodeEditorKeyDown(event: KeyboardEvent<HTMLTextAreaElement>, setCode: (value: string) => void) {
  if (event.key !== 'Tab') return;
  event.preventDefault();

  const textarea = event.currentTarget;
  const { selectionStart, selectionEnd, value } = textarea;
  const indent = '    ';

  if (event.shiftKey) {
    const lineStart = value.lastIndexOf('\n', selectionStart - 1) + 1;
    if (!value.slice(lineStart, lineStart + indent.length).startsWith(' ')) return;
    const removeCount = value.slice(lineStart, lineStart + indent.length).match(/^ {1,4}/)?.[0].length ?? 0;
    const nextValue = value.slice(0, lineStart) + value.slice(lineStart + removeCount);
    setCode(nextValue);
    requestAnimationFrame(() => {
      textarea.setSelectionRange(Math.max(lineStart, selectionStart - removeCount), Math.max(lineStart, selectionEnd - removeCount));
    });
    return;
  }

  const nextValue = value.slice(0, selectionStart) + indent + value.slice(selectionEnd);
  setCode(nextValue);
  const nextCursor = selectionStart + indent.length;
  requestAnimationFrame(() => textarea.setSelectionRange(nextCursor, nextCursor));
}

function SettingsStage({ soundEnabled, setSoundEnabled }: { soundEnabled: boolean; setSoundEnabled: (value: boolean) => void }) {
  return (
    <main className="settings-stage">
      <section className="settings-card">
        <h1>Settings</h1>
        <label className="toggle">
          <input type="checkbox" checked={soundEnabled} onChange={(event) => { localStorage.setItem('sound', event.target.checked ? 'on' : 'off'); setSoundEnabled(event.target.checked); }} />
          Optional sounds
        </label>
        <p>Sounds are generated locally and can stay off. The runner remains fully local; no AI services, telemetry, auth, or cloud database are used.</p>
      </section>
    </main>
  );
}

function unlockCopy(module: ModuleSummary) {
  if (module.id === 'devops') return 'Unlocks at Level 10.';
  if (module.id === 'ai-integration') return 'Unlocks after the Backend boss.';
  return `Unlocks at Level ${module.order}.`;
}

declare global {
  interface Window {
    webkitAudioContext?: typeof AudioContext;
  }
}
