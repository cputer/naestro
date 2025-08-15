import React from 'react';
import { Editor, DiffEditor } from '@monaco-editor/react';

const CodeEditor = ({ original = '', modified, language = 'javascript', height = '400px' }) => {
  if (modified !== undefined) {
    return (
      <DiffEditor
        original={original}
        modified={modified}
        height={height}
        language={language}
        options={{ renderSideBySide: true, automaticLayout: true }}
      />
    );
  }

  return (
    <Editor
      value={original}
      height={height}
      language={language}
      options={{ automaticLayout: true }}
    />
  );
};

export default CodeEditor;
