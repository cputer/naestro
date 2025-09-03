import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import { describe, it, expect, beforeAll, afterEach, afterAll } from "vitest";
import React, { useState } from "react";
import { server } from "../mocks/server.js";
import { http, HttpResponse } from "msw";

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

function OrchestrateFlow() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const resp = await fetch("http://localhost/api/orchestrate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    const data = await resp.json();
    setResult(data.result);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        placeholder="Prompt"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button type="submit">Run</button>
      {result && <div role="status">{result}</div>}
    </form>
  );
}

describe("Orchestrate flow", () => {
  it("submits prompt and displays final solution", async () => {
    server.use(
      http.post("http://localhost/api/orchestrate", () =>
        HttpResponse.json({ result: "FINAL_SOLUTION" }),
      ),
    );

    render(<OrchestrateFlow />);
    fireEvent.change(screen.getByPlaceholderText(/prompt/i), {
      target: { value: "test prompt" },
    });
    fireEvent.click(screen.getByRole("button", { name: /run/i }));
    const status = await screen.findByRole("status");
    expect(status).toHaveTextContent("FINAL_SOLUTION");
  });
});
