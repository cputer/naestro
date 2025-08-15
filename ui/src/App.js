import React from 'react';
import { Container, Grid, Paper, Typography } from '@mui/material';
import DiffViewer from './components/DiffViewer';
import MetricsChart from './components/MetricsChart';
import ServiceStatus from './components/ServiceStatus';

function App() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        NAESTRO Dashboard
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Code Diff
            </Typography>
            <DiffViewer
              original={"function add(a, b) { return a + b; }"}
              modified={"function add(a, b) { return a - b; }"}
            />
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              Metrics
            </Typography>
            <MetricsChart />
          </Paper>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Service Status
            </Typography>
            <ServiceStatus />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;

