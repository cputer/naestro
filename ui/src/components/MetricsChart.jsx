import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import io from "socket.io-client";
import { SOCKET_BASE_URL } from "../config";

/**
 * MetricsChart renders latency/throughput metrics.
 *
 * It optionally accepts a `getMetrics` function which can deterministically
 * push metrics to the chart (used in tests or for alternative data sources).
 * When omitted the component will subscribe to the default socket stream.
 *
 * @param {{getMetrics?: (emit: (m: any) => void) => (void|(() => void))}} props
 */
const MetricsChart = ({ getMetrics }) => {
  const [data, setData] = useState([]);
  const [error, setError] = useState(false);

  useEffect(() => {
    let cleanup = () => {};

    const emit = (metrics) => {
      if (Array.isArray(metrics)) {
        metrics.forEach((m) =>
          setData((prev) => [...prev.slice(-19), m])
        );
      } else if (metrics) {
        setData((prev) => [...prev.slice(-19), metrics]);
      }
    };

    const setup = async () => {
      try {
        if (getMetrics) {
          const result = await getMetrics(emit);
          if (typeof result === "function") cleanup = result;
        } else {
          const socket = io(SOCKET_BASE_URL);
          socket.on("metrics", emit);
          socket.on("connect_error", () => setError(true));
          cleanup = () => socket.close();
        }
      } catch {
        setError(true);
      }
    };

    setup();

    return () => {
      cleanup();
    };
  }, [getMetrics]);

  if (error) {
    return <div role="alert">Error loading metrics</div>;
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="latency" stroke="#8884d8" />
        <Line type="monotone" dataKey="throughput" stroke="#82ca9d" />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default MetricsChart;
