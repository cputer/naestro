import React, { useEffect, useState } from 'react';
import { Chip, Stack } from '@mui/material';
import io from 'socket.io-client';

const ServiceStatus = () => {
  const [status, setStatus] = useState({});

  useEffect(() => {
    const socket = io('http://localhost:4000');
    socket.on('status', (s) => setStatus(s));
    return () => socket.close();
  }, []);

  return (
    <Stack direction="row" spacing={1}>
      {Object.entries(status).map(([name, state]) => (
        <Chip key={name} label={`${name}: ${state}`} color={state === 'online' ? 'success' : 'error'} />
      ))}
    </Stack>
  );
};

export default ServiceStatus;
