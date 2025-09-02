/* eslint-env browser */
import React from 'react';
import PropTypes from 'prop-types';

export default function CodeEditor({
  original = '',
  modified = '',
  language = 'plaintext',
  height = 320
}) {
  // Lightweight placeholder; replace with Monaco later if desired
  return (
    <div style={{ display: 'grid', gap: 12 }}>
      <div>
        <div style={{ fontSize: 12, opacity: 0.7 }}>Original ({language})</div>
        <pre style={{ height, overflow: 'auto', border: '1px solid #333', padding: 12, borderRadius: 8 }}>
          {original}
        </pre>
      </div>
      <div>
        <div style={{ fontSize: 12, opacity: 0.7 }}>Modified ({language})</div>
        <pre style={{ height, overflow: 'auto', border: '1px solid #333', padding: 12, borderRadius: 8 }}>
          {modified}
        </pre>
      </div>
    </div>
  );
}

CodeEditor.propTypes = {
  original: PropTypes.string,
  modified: PropTypes.string,
  language: PropTypes.string,
  height: PropTypes.oneOfType([PropTypes.number, PropTypes.string])
};
