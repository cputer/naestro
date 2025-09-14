import React, { useEffect, useState } from 'react';

export type CollaborationPrefs = {
  mode: string;
  depth: number;
  auto: boolean;
  ask_online: boolean;
  budget_usd: number;
  p95_latency_s: number;
  answer_strategy: string;
  confidence_threshold: number;
};

const DEFAULT_PREFS: CollaborationPrefs = {
  mode: 'consult',
  depth: 1,
  auto: true,
  ask_online: true,
  budget_usd: 0.5,
  p95_latency_s: 20,
  answer_strategy: 'self_if_confident',
  confidence_threshold: 0.7,
};

interface Props {
  loadPrefs?: () => Promise<Partial<CollaborationPrefs>>;
  savePrefs?: (prefs: CollaborationPrefs) => Promise<Partial<CollaborationPrefs>>;
}

const CollaborationPanel: React.FC<Props> = ({ loadPrefs, savePrefs }) => {
  const [prefs, setPrefs] = useState<CollaborationPrefs>(DEFAULT_PREFS);
  const [status, setStatus] = useState<'saving' | 'saved' | 'error' | null>(null);

  // Load preferences on mount
  useEffect(() => {
    const loader = loadPrefs
      ? loadPrefs
      : () => fetch('/orchestrator/prefs').then((r) => r.json());
    loader()
      .then((data) => setPrefs({ ...DEFAULT_PREFS, ...(data as any) }))
      .catch(() => setStatus('error'));
  }, [loadPrefs]);

  const handleChange = <K extends keyof CollaborationPrefs>(key: K, value: CollaborationPrefs[K]) => {
    setPrefs((prev) => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    setStatus('saving');
    const saver = savePrefs
      ? savePrefs
      : (p: CollaborationPrefs) =>
          fetch('/orchestrator/prefs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(p),
          }).then((r) => r.json());
    try {
      const data = await saver(prefs);
      setPrefs((prev) => ({ ...prev, ...(data as any) }));
      setStatus('saved');
    } catch {
      setStatus('error');
    }
  };

  return (
    <div>
      <h3>Collaboration Preferences</h3>
      <div>
        <label>
          Mode
          <select
            value={prefs.mode}
            onChange={(e) => handleChange('mode', e.target.value)}
          >
            <option value="solo">solo</option>
            <option value="consult">consult</option>
            <option value="collaborate">collaborate</option>
            <option value="consensus">consensus</option>
            <option value="swarm">swarm</option>
          </select>
        </label>
      </div>
      <div>
        <label>
          Depth
          <input
            type="number"
            value={prefs.depth}
            min={0}
            max={3}
            onChange={(e) => handleChange('depth', Number(e.target.value) || 0)}
          />
        </label>
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={prefs.auto}
            onChange={(e) => handleChange('auto', e.target.checked)}
          />
          Auto escalate
        </label>
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={prefs.ask_online}
            onChange={(e) => handleChange('ask_online', e.target.checked)}
          />
          Ask online
        </label>
      </div>
      <div>
        <label>
          Budget USD
          <input
            type="number"
            value={prefs.budget_usd}
            min={0}
            step={0.01}
            onChange={(e) => handleChange('budget_usd', Number(e.target.value) || 0)}
          />
        </label>
      </div>
      <div>
        <label>
          P95 latency (s)
          <input
            type="number"
            value={prefs.p95_latency_s}
            min={0}
            onChange={(e) => handleChange('p95_latency_s', Number(e.target.value) || 0)}
          />
        </label>
      </div>
      <div>
        <label>
          Answer strategy
          <select
            value={prefs.answer_strategy}
            onChange={(e) => handleChange('answer_strategy', e.target.value)}
          >
            <option value="self_if_confident">self_if_confident</option>
            <option value="aggregate_always">aggregate_always</option>
            <option value="ask_clarify_below_threshold">ask_clarify_below_threshold</option>
          </select>
        </label>
      </div>
      <div>
        <label>
          Confidence threshold
          <input
            type="number"
            value={prefs.confidence_threshold}
            min={0}
            max={1}
            step={0.01}
            onChange={(e) =>
              handleChange('confidence_threshold', Number(e.target.value) || 0)
            }
          />
        </label>
      </div>
      <button onClick={handleSave}>Save</button>
      {status === 'saved' && <div role="status">Saved</div>}
      {status === 'error' && <div role="alert">Error</div>}
    </div>
  );
};

export default CollaborationPanel;

