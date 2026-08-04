import type { ConceptPanel as ConceptPanelData, DiagramSpec } from '../types/content';

export function ConceptPanel({ panel }: { panel?: ConceptPanelData }) {
  if (!panel) return null;
  return (
    <aside className="concept-panel" aria-label={`Concept: ${panel.title}`}>
      <div className="concept-header">
        <span>Concept</span>
        <h2>{panel.title}</h2>
      </div>
      <p>{panel.explanation}</p>
      <Diagram diagram={panel.diagram} />
      <div className="concept-section">
        <span>Key takeaways</span>
        <ul>
          {panel.key_takeaways.map((item) => <li key={item}>{item}</li>)}
        </ul>
      </div>
      <div className="concept-callout">
        <span>Practical example</span>
        <p>{panel.practical_example}</p>
      </div>
      <div className="concept-interview">
        <span>Interview insight</span>
        <p>{panel.interview_insight}</p>
      </div>
    </aside>
  );
}

function Diagram({ diagram }: { diagram?: DiagramSpec }) {
  if (!diagram) return null;
  if (diagram.type === 'compare') return <CompareDiagram diagram={diagram} />;
  if (diagram.type === 'network') return <NetworkDiagram diagram={diagram} />;
  if (diagram.type === 'triangle') return <TriangleDiagram diagram={diagram} />;
  return <FlowDiagram diagram={diagram} />;
}

function FlowDiagram({ diagram }: { diagram: DiagramSpec }) {
  const nodes = diagram.nodes ?? [];
  return (
    <div className="concept-diagram flow-diagram">
      {diagram.title && <strong>{diagram.title}</strong>}
      <div>
        {nodes.map((node, index) => (
          <div className="flow-step" key={`${node.id ?? node.label}-${index}`}>
            <span className={node.status}>{node.label}</span>
            {index < nodes.length - 1 && <i />}
          </div>
        ))}
      </div>
    </div>
  );
}

function CompareDiagram({ diagram }: { diagram: DiagramSpec }) {
  return (
    <div className="concept-diagram compare-diagram">
      {diagram.title && <strong>{diagram.title}</strong>}
      <div>
        {(diagram.columns ?? []).map((column) => (
          <section key={column.title}>
            <b>{column.title}</b>
            {column.items.map((item) => <span key={item}>{item}</span>)}
          </section>
        ))}
      </div>
    </div>
  );
}

function NetworkDiagram({ diagram }: { diagram: DiagramSpec }) {
  const nodes = diagram.nodes ?? [];
  const edges = diagram.edges ?? [];
  return (
    <div className="concept-diagram network-diagram">
      {diagram.title && <strong>{diagram.title}</strong>}
      <div className="network-nodes">
        {nodes.map((node) => <span key={node.id ?? node.label} className={node.status}>{node.label}</span>)}
      </div>
      {edges.length > 0 && (
        <div className="network-edges">
          {edges.map((edge) => <small key={`${edge.from}-${edge.to}-${edge.label ?? ''}`}>{edge.from} {'->'} {edge.to}{edge.label ? ` · ${edge.label}` : ''}</small>)}
        </div>
      )}
    </div>
  );
}

function TriangleDiagram({ diagram }: { diagram: DiagramSpec }) {
  const points = diagram.points ?? [];
  return (
    <div className="concept-diagram triangle-diagram">
      {diagram.title && <strong>{diagram.title}</strong>}
      <div>
        {points.slice(0, 3).map((point) => <span key={point.label}>{point.label}</span>)}
      </div>
    </div>
  );
}
