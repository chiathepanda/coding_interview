import React from 'react';
import { Modal, Box, Button, Typography } from '@mui/material';

const DeleteWarning = ({ isOpen, onCancel, onContinue, continueText, content }) => {
  return (
    <Modal open={isOpen} onClose={onCancel}>
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
        <Typography variant="h6">{content}</Typography>
        <Box mt={2} display="flex" justifyContent="space-between">
          <Button variant="contained" color="error" onClick={onContinue}>
            {continueText}
          </Button>
          <Button variant="outlined" onClick={onCancel}>
            Cancel
          </Button>
        </Box>
      </Box>
    </Modal>
  );
};

export default DeleteWarning;