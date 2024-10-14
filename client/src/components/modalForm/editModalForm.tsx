import React, { useState } from 'react';
import { Formik, Form } from 'formik';

import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import { Button, Typography } from '@mui/material';

import renderFields from './renderFields';
import LogoUpload from './LogoUpload';  // Import the new component
import DeleteWarning from '../generic/warning';

import { flattenKeys } from '../utils';


const EditFormModal = ({ isOpen, onClose, errorMessage, rowData, handleSubmit, fieldConfigs, formSchema, hasFileUpload, dropdownFieldValues }) => {
  const [filePreview, setFilePreview] = useState(rowData && rowData.logo ? `${import.meta.env.VITE_API_URL}/${rowData.logo}` : "");
  const [isEditWarningOpen, setIsEditWarningOpen] = useState(false);
  const isCreate = rowData == null;

  const initialValues = isCreate
    ? fieldConfigs.reduce((acc, field) => {
      acc[field.name] = null;
      return flattenKeys(acc);
    }, {})
    : flattenKeys(rowData);

  const handleCancel = (dirty) => {
    if (dirty) {
      setIsEditWarningOpen(true);
    } else {
      onClose();
    }
  };

  return (
    <Dialog open={isOpen} onClose={onClose}>
      <DialogTitle>{isCreate ? 'Add Row' : 'Edit Row'}</DialogTitle>
      <DialogContent>
        <Formik
          initialValues={initialValues}
          validationSchema={formSchema}
          onSubmit={async (values, { setSubmitting, setErrors, setStatus }) => {
            try {
              await handleSubmit(values);
              setStatus(null); // Clear any existing status messages if submission is successful
            } catch (error) {
              setStatus(error.message || "An error occurred while saving the form.");
            } finally {
              setSubmitting(false);  // Stop the submitting state
            }
          }}
        >
          {({ setFieldValue, handleChange, handleBlur, values, submitCount, dirty }) => (
            <Form>
              {/* Conditionally insert the LogoUpload component */}
              {hasFileUpload && (
                <LogoUpload
                  name="logo"
                  filePreview={filePreview}
                  setFilePreview={setFilePreview}
                  setFieldValue={setFieldValue}
                />
              )}

              {renderFields(setFieldValue, handleChange, handleBlur, values, fieldConfigs, dropdownFieldValues)}

              {errorMessage && submitCount > 0 && (
                <div id="errorMessage" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  {errorMessage && (
                    <Typography color="error">
                      {errorMessage}
                    </Typography>
                  )}
                </div>
              )}

              {
                isEditWarningOpen &&
                (
                  <DeleteWarning
                    isOpen={isEditWarningOpen}
                    onCancel={() => setIsEditWarningOpen(false)}
                    onContinue={onClose}
                    continueText="YES"
                    content='The form has been edited. Are you sure you want to go back?'
                  />)
              }
              <DialogActions>
                <Button onClick={() => handleCancel(dirty)} color="secondary">
                  Cancel
                </Button>
                <Button type="submit" color="primary" variant="contained">
                  {isCreate ? 'Create' : 'Save'}
                </Button>
              </DialogActions>
            </Form>
          )}
        </Formik>
      </DialogContent>
    </Dialog>
  );
};

export default EditFormModal;
