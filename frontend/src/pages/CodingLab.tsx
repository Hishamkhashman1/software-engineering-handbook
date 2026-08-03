import { useState } from 'react';
import { api } from '../api/client';
import { useAsync } from '../hooks/useAsync';

export function CodingLab() {
  const modules = useAsync(api.modules, []);
  const [moduleId, setModuleId] = useState('');
  const detail = useAsync(() => moduleId ? api.module(moduleId) : Promise.resolve(null), [moduleId]);
  const challenge = detail.data?.coding_challenges[0];
  const [code, setCode] = useState('');
  const [result, setResult] = useState<object | null>(null);

  return (
    <section>
      <h1>Coding Lab</h1>
      <div className="panel controls">
        <label>Module
          <select value={moduleId} onChange={(event) => { setModuleId(event.target.value); setCode(''); setResult(null); }}>
            <option value="">Select a module</option>
            {modules.data?.map((module) => <option key={module.id} value={module.id}>{module.title}</option>)}
          </select>
        </label>
      </div>
      {challenge && (
        <div className="grid two">
          <div className="panel">
            <h2>{challenge.title}</h2>
            <p>{challenge.instructions}</p>
            <h3>Visible tests</h3>
            {challenge.visible_tests.map((test) => <pre key={test.name}>{test.call} == {JSON.stringify(test.expected)}</pre>)}
          </div>
          <div className="panel">
            <textarea className="code-editor" value={code || challenge.starter_code} onChange={(event) => setCode(event.target.value)} />
            <button className="primary" onClick={async () => setResult(await api.runCode(moduleId, challenge.id, code || challenge.starter_code))}>Run tests</button>
            {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
          </div>
        </div>
      )}
    </section>
  );
}
