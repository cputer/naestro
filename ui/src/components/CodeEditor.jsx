import React from 'react';
import PropTypes from 'prop-types';
import { Editor, DiffEditor } from '@monaco-editor/react';

const CodeEditor = ({ original, modified, language = 'javascript', height }) => {
  if (modified) {
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

CodeEditor.propTypes = {
  language: PropTypes.string.isRequired,
  original: PropTypes.string,
  modified: PropTypes.string,
  height: PropTypes.oneOfType([PropTypes.number, PropTypes.string])
};
CodeEditor.defaultProps = {
  original: '',
  modified: '',
  height: 400
};

export default CodeEditor;
