import React from 'react';
import { CatchBoundary, createRootRoute, Link, Outlet, useLocation } from '@tanstack/react-router';
import { TanStackRouterDevtools } from '@tanstack/router-devtools';
import { AppBar, Toolbar, Button, Divider } from '@mui/material';


export const Route = createRootRoute({
  component: () => {
    const location = useLocation();

    return (<>
      <AppBar position="static" color="default">
        <Toolbar>
          <Button component={Link} to="/" className="[&.active]:font-bold" color="inherit" >
            Home
          </Button>
          <Button component={Link} to="/cafes" className="[&.active]:font-bold" color="inherit" >
            Cafes
          </Button>
          <Button component={Link} to="/employees" className="[&.active]:font-bold" color="inherit" >
            Employees
          </Button>
        </Toolbar>
      </AppBar>

      <Divider sx={{ my: 2 }} />

      <CatchBoundary
        getResetKey={() => location.pathname}
        onCatch={(error) => console.error(error)}
      >
        <Outlet />
      </CatchBoundary>

      <TanStackRouterDevtools />
    </>)
  }
});
