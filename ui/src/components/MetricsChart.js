import React, { useEffect, useState } from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import io from 'socket.io-client';

const MetricsChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const socket = io('http://localhost:4000');
    socket.on('metrics', (metrics) => {
      setData((prev) => [...prev.slice(-19), metrics]);
    });
    return () => socket.close();
  }, []);

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
