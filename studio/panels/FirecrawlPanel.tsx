import React, { useEffect, useState } from 'react';

const FirecrawlPanel: React.FC = () => {
  const [url, setUrl] = useState('');
  const [mode, setMode] = useState('crawl');
  const [depth, setDepth] = useState(1);
  const [includeGlobs, setIncludeGlobs] = useState('');
  const [excludeGlobs, setExcludeGlobs] = useState('');
  const [qps, setQps] = useState(1);
  const [respectRobots, setRespectRobots] = useState(true);
  const [includeSubdomains, setIncludeSubdomains] = useState(false);
  const [includePdfs, setIncludePdfs] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [cost, setCost] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const [retries, setRetries] = useState(0);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    let timer: NodeJS.Timeout | undefined;
    if (running) {
      timer = setInterval(() => {
        setElapsed((t) => t + 1);
        setCost((c) => c + qps * 0.001);
        setRetries((r) => r + (Math.random() < 0.1 ? 1 : 0));
        setLogs((l) =>
          [...l, `Fetched ${url || 'unknown'} at ${new Date().toISOString()}`].slice(-100),
        );
      }, 1000);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [running, url, qps]);

  const handleStart = () => {
    setRunning(true);
    setLogs([]);
    setElapsed(0);
    setCost(0);
    setRetries(0);
  };

  const handleStop = () => {
    setRunning(false);
  };

  const handleExport = () => {
    const flow = {
      name: 'Firecrawl',
      parameters: {
        url,
        mode,
        depth,
        includeGlobs,
        excludeGlobs,
        qps,
        respectRobots,
        includeSubdomains,
        includePdfs,
      },
    };
    const blob = new Blob([JSON.stringify(flow, null, 2)], { type: 'application/json' });
    const href = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = href;
    a.download = 'firecrawl-n8n-flow.json';
    a.click();
    URL.revokeObjectURL(href);
  };

  return (
    <div className="firecrawl-panel">
      <h2>Firecrawl</h2>
      <div>
        <label>
          URL
          <input type="text" value={url} onChange={(e) => setUrl(e.target.value)} />
        </label>
      </div>
      <div>
        <label>
          Mode
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="crawl">Crawl</option>
            <option value="single">Single Page</option>
          </select>
        </label>
      </div>
      <div>
        <label>
          Depth
          <input
            type="number"
            value={depth}
            min={0}
            onChange={(e) => setDepth(parseInt(e.target.value, 10) || 0)}
          />
        </label>
      </div>
      <div>
        <label>
          Include globs
          <input
            type="text"
            value={includeGlobs}
            onChange={(e) => setIncludeGlobs(e.target.value)}
            placeholder="e.g. **/*.html"
          />
        </label>
      </div>
      <div>
        <label>
          Exclude globs
          <input
            type="text"
            value={excludeGlobs}
            onChange={(e) => setExcludeGlobs(e.target.value)}
            placeholder="e.g. **/*.png"
          />
        </label>
      </div>
      <div>
        <label>
          QPS
          <input
            type="number"
            value={qps}
            min={0}
            onChange={(e) => setQps(parseInt(e.target.value, 10) || 0)}
          />
        </label>
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={respectRobots}
            onChange={(e) => setRespectRobots(e.target.checked)}
          />
          Respect robots.txt
        </label>
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={includeSubdomains}
            onChange={(e) => setIncludeSubdomains(e.target.checked)}
          />
          Include subdomains
        </label>
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={includePdfs}
            onChange={(e) => setIncludePdfs(e.target.checked)}
          />
          Include PDFs
        </label>
      </div>
      <div className="actions">
        {running ? (
          <button onClick={handleStop}>Stop</button>
        ) : (
          <button onClick={handleStart}>Start</button>
        )}
        <button onClick={handleExport}>Export n8n flow</button>
      </div>
      <div className="estimates">
        <p>Elapsed: {elapsed}s</p>
        <p>Estimated cost: ${cost.toFixed(4)}</p>
        <p>Retries: {retries}</p>
      </div>
      <div className="logs">
        <h3>Logs</h3>
        <pre style={{ maxHeight: '200px', overflow: 'auto' }}>{logs.join('\n')}</pre>
      </div>
    </div>
  );
};

export default FirecrawlPanel;

