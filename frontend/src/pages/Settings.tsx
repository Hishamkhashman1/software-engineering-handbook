import { api } from '../api/client';

export function Settings() {
  return (
    <section>
      <h1>Settings</h1>
      <div className="panel">
        <h2>Local data</h2>
        <p>Progress is stored in SQLite at data/interview_game.db. Content is loaded from JSON files in content/.</p>
        <button className="danger" onClick={async () => { await api.reset(); window.location.reload(); }}>Reset progress</button>
      </div>
      <div className="panel">
        <h2>Code runner boundary</h2>
        <p>The Python runner uses temporary directories, timeouts, subprocess execution, and import checks. It is a local learning sandbox, not a hardened multi-user security boundary.</p>
      </div>
    </section>
  );
}
