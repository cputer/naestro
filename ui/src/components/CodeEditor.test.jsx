import { describe, it, expect } from 'vitest';
import React from 'react';
import ReactDOMServer from 'react-dom/server';
import CodeEditor from './CodeEditor';

describe('CodeEditor', () => {
  it('renders labels for original and modified code', () => {
    const html = ReactDOMServer.renderToStaticMarkup(
      <CodeEditor original="foo" modified="bar" language="python" />
    );

    expect(html).toContain('Original (python)');
    expect(html).toContain('Modified (python)');
  });
});
