import '@testing-library/jest-dom';

const originalError = console.error;
console.error = (...args) => {
  if (typeof args[0] === 'string' && args[0].includes('ReactDOM.render is no longer supported in React 18')) {
    return;
  }
  originalError(...args);
};
