import React from 'react';
import PropTypes from 'prop-types';

export default function CodeEditor({
  language = 'javascript',
  original = '',
  modified = '',
  height = 400
}) {
  const px = typeof height === 'number' ? `${height}px` : (height || '400px');
  return (
    <div style={{ height: px, border: '1px solid #222', borderRadius: 8 }}>
      <div style={{ padding: 8, fontFamily: 'monospace', fontSize: 12 }}>
        <div><strong>Language:</strong> {language || 'plaintext'}</div>
        <div style={{ marginTop: 8 }}>
          <strong>Original:</strong>
          <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{original}</pre>
        </div>
        <div style={{ marginTop: 8 }}>
          <strong>Modified:</strong>
          <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{modified}</pre>
        </div>
      </div>
    </div>
  );
}

CodeEditor.propTypes = {
  language: PropTypes.string,
  original: PropTypes.string,
  modified: PropTypes.string,
  height: PropTypes.oneOfType([PropTypes.number, PropTypes.string])
};
