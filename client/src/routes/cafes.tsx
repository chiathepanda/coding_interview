import React from 'react';

import { createFileRoute, Link } from '@tanstack/react-router';

import GridTemplate from '../components/generic/gridTemplate';

import { addCafe, editCafe, deleteCafe } from '../api/cafes';
import { cafeFieldConfigs } from '../formConfigs/cafeFieldConfigs';
import { cafeSchema } from '../../validation/schemas/cafeSchema';

import { useFetchCafes } from '../hooks/cafe/useFetchCafes';

export const Route = createFileRoute('/cafes')({
  component: Cafes,
});

function Cafes() {
  const { data: cafes, isLoading, isError } = useFetchCafes();

  // Column definition for the grid
  const colDefs = [
    {
      field: 'logo',
      headerName: 'Logo',
      cellRenderer: (params) => {
        return params.data.logo ?
          <div className="logo-container">
            <img src={`${import.meta.env.VITE_API_URL}/${params.data.logo}`} style={{ width: '80px', height: '80px' }} />
          </div> : null;
      },
      autoHeight: true
    },
    { field: 'name', headerName: 'Name' },
    {
      field: 'description', headerName: 'Description',
      tooltipValueGetter: (params) => {
        return `${params.value}`;
      },
    },
    { field: 'location', filter: true, headerName: 'Location' },
    {
      field: 'employees',
      headerName: 'Employees',
      cellRenderer: (params) => {
        return params.data.employees == 0 ? 0 : <Link to={params.data.employees > 0 ? `/employees?cafe_id=${params.data.id}` : ""}>{params.data.employees}</Link>;
      },
    },

  ];

  // Handle loading and error states
  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error loading cafes</div>;


  return (
    <div className="p-2">
      <GridTemplate
        queryKey="cafes"
        model="cafe"
        rowData={cafes}
        colDefs={colDefs}
        hooks={{
          addHook: addCafe,
          editHook: editCafe,
          deleteHook: deleteCafe,
        }}
        fieldConfigs={cafeFieldConfigs}
        formSchema={cafeSchema}
        hasFileUpload={true}
        dropdownFieldValues={{}}
      />
    </div>
  );
}
