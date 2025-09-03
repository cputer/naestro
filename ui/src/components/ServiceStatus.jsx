import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { Chip, Stack } from '@mui/material';

const colorMap = {
  ok: 'success',
  degraded: 'warning',
  down: 'error'
};

export default function ServiceStatus({ status, getStatus }) {
  const [internalStatus, setInternalStatus] = useState(status ?? {});

  useEffect(() => {
    if (!status && typeof getStatus === 'function') {
      getStatus()
        .then((data) => setInternalStatus(data))
        .catch(() => setInternalStatus({}));
    }
  }, [status, getStatus]);

  const current = status ?? internalStatus;

  const colorFor = (state) => colorMap[state] ?? 'default';

  return (
    <Stack direction="row" spacing={1}>
      {Object.entries(current).map(([name, state]) => (
        <Chip key={name} label={`${name}: ${state}`} color={colorFor(state)} />
      ))}
    </Stack>
  );
}

ServiceStatus.propTypes = {
  status: PropTypes.object,
  getStatus: PropTypes.func
};
