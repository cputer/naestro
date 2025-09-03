import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { http, HttpResponse } from "msw";
import { server } from "../../mocks/server.js";
import ServiceStatus from "../ServiceStatus.jsx";

describe("ServiceStatus", () => {
  it.each([
    ["ok", "MuiChip-colorSuccess"],
    ["degraded", "MuiChip-colorWarning"],
    ["down", "MuiChip-colorError"],
  ])("renders %s status", (state, className) => {
    render(<ServiceStatus status={{ svc: state }} />);
    const chip = screen.getByText(`svc: ${state}`).closest(".MuiChip-root");
    expect(chip).toHaveClass(className);
  });

  it("fetches service status and renders chips with correct colors", async () => {
    server.use(
      http.get("/api/status", () =>
        HttpResponse.json({
          api: "ok",
          db: "degraded",
          auth: "down",
        }),
      ),
    );
    const getStatus = () => fetch("/api/status").then((r) => r.json());
    render(<ServiceStatus getStatus={getStatus} />);

    const cases = [
      ["api", "ok", "MuiChip-colorSuccess"],
      ["db", "degraded", "MuiChip-colorWarning"],
      ["auth", "down", "MuiChip-colorError"],
    ];

    for (const [name, state, className] of cases) {
      const chip = await screen.findByText(`${name}: ${state}`);
      expect(chip.closest(".MuiChip-root")).toHaveClass(className);
    }
  });

  it("handles network error", async () => {
    server.use(http.get("/status", () => HttpResponse.error()));
    const getStatus = () => fetch("/status").then((r) => r.json());
    const { container } = render(<ServiceStatus getStatus={getStatus} />);
    await waitFor(() => {
      expect(container.querySelector(".MuiChip-root")).toBeNull();
    });
  });
});
