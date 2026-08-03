import { BarChart3, BookOpen, Code2, Gauge, Home, RotateCcw, Settings, Timer } from 'lucide-react';

const items = [
  ['dashboard', 'Dashboard', Home],
  ['modules', 'Modules', BookOpen],
  ['quiz', 'Quick Quiz', Gauge],
  ['review', 'Weak Review', RotateCcw],
  ['interview', 'Interview', Timer],
  ['coding', 'Coding Lab', Code2],
  ['progress', 'Progress', BarChart3],
  ['settings', 'Settings', Settings]
] as const;

export function Nav({ view, setView }: { view: string; setView: (view: string) => void }) {
  return (
    <nav className="nav">
      <div className="brand">Interview Game</div>
      {items.map(([id, label, Icon]) => (
        <button key={id} className={view === id ? 'active' : ''} onClick={() => setView(id)}>
          <Icon size={18} />
          {label}
        </button>
      ))}
    </nav>
  );
}
