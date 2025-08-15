import React, { useEffect, useRef } from 'react';
import * as monaco from 'monaco-editor';

const DiffViewer = ({ original = '', modified = '' }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current) {
      const editor = monaco.editor.createDiffEditor(containerRef.current, {
        automaticLayout: true,
      });
      const originalModel = monaco.editor.createModel(original, 'javascript');
      const modifiedModel = monaco.editor.createModel(modified, 'javascript');
      editor.setModel({ original: originalModel, modified: modifiedModel });
      return () => {
        originalModel.dispose();
        modifiedModel.dispose();
        editor.dispose();
      };
    }
  }, [original, modified]);

  return <div style={{ height: '400px', border: '1px solid #eee' }} ref={containerRef} />;
};

export default DiffViewer;
