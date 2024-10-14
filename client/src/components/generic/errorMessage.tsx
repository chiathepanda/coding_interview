import React from 'react';
import { Modal, Box, Button, Typography } from '@mui/material';

const ErrorMessage = ({ isOpen, onClose, errorMessage }) => {
  return (
    <Modal open={isOpen} onClose={onClose}>
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          bgcolor: 'background.paper',
          p: 4,
          borderRadius: '8px',
        }}
      >
        <Typography variant="h6">{errorMessage}</Typography>
        <Box mt={2} display="flex" justifyContent="space-between">
          <Button variant="outlined" onClick={onClose}>
            OK
          </Button>
        </Box>
      </Box>
    </Modal>
  );
};

export default ErrorMessage;