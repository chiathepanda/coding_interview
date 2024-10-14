import React, { useState, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { useQueryClient } from '@tanstack/react-query';
import Box from '@mui/material/Box';
import { Button } from '@mui/material';
import EditFormModal from '../modalForm/editModalForm';
import DeleteIcon from '@mui/icons-material/Delete';
import DeleteWarning from './warning';

const GridTemplate = ({ queryKey, model, rowData, colDefs, hooks, fieldConfigs, formSchema, hasFileUpload, dropdownFieldValues }) => {
  const { addHook, editHook, deleteHook } = hooks;
  const queryClient = useQueryClient();
  const [errorMessage, setErrorMessage] = useState('');
  const [selectedRow, setSelectedRow] = useState<Object | null>(null);

  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteWarningOpen, setIsDeletelWarningOpen] = useState(false);

  const openAddModal = () => {
    setSelectedRow(null);
    setIsEditModalOpen(true);
  };

  const openEditModal = (data) => {
    setSelectedRow(data);
    setIsEditModalOpen(true);
  };

  const deleteItem = (data) => {
    setSelectedRow(data);
    setIsDeletelWarningOpen(true);
  };

  const handleAdd = async (newData) => {
    try {
      await addHook(
        newData
      );
      setIsEditModalOpen(false);
      queryClient.invalidateQueries({ queryKey: [queryKey] });
    } catch (error) {
      setErrorMessage(error.message);
    }
  };

  const handleSave = async (updatedData) => {
    if (!selectedRow) {
      return;
    }
    try {
      await editHook(
        updatedData,
      );
      setIsEditModalOpen(false);
      queryClient.invalidateQueries({ queryKey: [queryKey] });
    } catch (error) {
      console.error(error.message);
    }
  };

  const handleDelete = async () => {
    try {
      await deleteHook(
        selectedRow.id,
      )

      setIsDeletelWarningOpen(false);
      queryClient.invalidateQueries({ queryKey: [queryKey] });

    } catch (error) {
      console.error('Failed to delete cafe:', error);
    }
  };

  const customColDefs = [
    ...colDefs,
    {
      field: 'actions',
      headerName: 'Actions',
      cellRenderer: (params) => {
        return (
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', height: '100%' }}>
            <Button
              variant="contained"
              disableElevation
              size="small"
              onClick={() => openEditModal(params.data)}
            >
              Edit
            </Button>
            <Button
              variant="contained"
              disableElevation
              size="small"
              color="error"
              startIcon={<DeleteIcon />}
              onClick={() => deleteItem(params.data)}
            >
              Delete
            </Button>
          </Box>
        );
      },
    },
  ];

  return (
    <>
      <div>
        <h1 style={{ display: 'inline-block', margin: 0, verticalAlign: 'bottom', marginBottom: 12 }}>{model ? model.charAt(0).toUpperCase() + model.slice(1) : model}</h1>
        {/* ADD BUTTON */}
        <Button
          variant="contained"
          disableElevation
          style={{ display: 'inline-block', verticalAlign: 'bottom', float: 'right' }}
          onClick={() => openAddModal()}
        >
          Add {model}
        </Button>

        <div className="ag-theme-alpine" style={{ height: 400, width: '100%' }}>
          {/* Table */}
          <AgGridReact
            rowData={rowData}
            columnDefs={customColDefs}
            gridOptions={{
              enableBrowserTooltips: true,
              pagination: true,
              onGridReady: function (params) {
                params.api.sizeColumnsToFit();
                window.addEventListener('resize', () => {
                  params.api.sizeColumnsToFit();
                });
              }
            }
            }
          />
        </div>
      </div>

      {/* Modals */}
      {
        isEditModalOpen && (
          <EditFormModal
            isOpen={isEditModalOpen}
            onClose={() => {
              setIsEditModalOpen(false);
              setErrorMessage('');
            }}
            errorMessage={errorMessage}
            rowData={selectedRow}
            handleSubmit={selectedRow == null ? handleAdd : handleSave}
            fieldConfigs={fieldConfigs}
            formSchema={formSchema}
            hasFileUpload={hasFileUpload}
            dropdownFieldValues={dropdownFieldValues}
          />
        )
      }

      {
        isDeleteWarningOpen && selectedRow &&
        (
          <DeleteWarning
            isOpen={isDeleteWarningOpen}
            onCancel={() => setIsDeletelWarningOpen(false)}
            onContinue={handleDelete}
            continueText="DELETE"
            content='Are you sure you want to delete this item?'
          />)
      }
    </>
  );
};

export default GridTemplate;