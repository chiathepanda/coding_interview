import React from 'react'
import { createFileRoute, useMatch } from '@tanstack/react-router'

import GridTemplate from '../components/generic/gridTemplate'

import { addEmployee, editEmployee, deleteEmployee } from '../api/employees'
import { employeeFieldConfigs } from '../formConfigs/employeeFieldConfigs'
import { employeeSchema } from '../../validation/schemas/employeeSchema'

import { useFetchEmployees } from '../hooks/employee/useFetchEmployees'
import { useFetchCafes } from '../hooks/cafe/useFetchCafes'

export const Route = createFileRoute('/employees')({
  component: Employees,
})

function Employees() {
  const match = useMatch({ from: '/employees' }) // Get the match object for the current route
  const cafe_id = match.search?.cafe_id

  const {
    data: employees,
    isLoading,
    isError,
  } = useFetchEmployees(true, cafe_id ? { cafe_id: cafe_id } : null)
  const {
    data: cafes,
    isLoading: isLoadingCafe,
    isError: isCafeError,
  } = useFetchCafes()

  // grid column definition
  const colDefs = [
    { field: 'name', headerName: 'Name' },
    { field: 'email_address', headerName: 'Email Address' },
    { field: 'phone_number', filter: true, headerName: 'Phone Number' },
    { field: 'days_worked', filter: true, headerName: 'Days Worked' },
    { field: 'cafe_relation.name', filter: true, headerName: 'Cafe' },
  ]

  // Handle loading and error states
  if (isLoading || isLoadingCafe) return <div>Loading...</div>
  if (isError || isCafeError) {
    throw new Error('Error loading Employees')
  }

  const updatedEmployeeFieldConfigs = employeeFieldConfigs.map((field) => {
    // Check if the field is the cafe dropdown
    if (field.name === 'cafe_relation.cafe_id') {
      // Append the new dynamic data to the options array
      return {
        ...field,
        options: cafes.map((cafe) => ({
          value: cafe.id,
          label: cafe.name,
        })),
      }
    }
    return field
  })

  return (
    <div className="p-2">
      <GridTemplate
        queryKey="employees"
        model="employee"
        rowData={employees}
        colDefs={colDefs}
        hooks={{
          addHook: addEmployee,
          editHook: editEmployee,
          deleteHook: deleteEmployee,
        }}
        fieldConfigs={updatedEmployeeFieldConfigs}
        formSchema={employeeSchema}
        hasFileUpload={false}
        dropdownFieldValues={{
          'cafe_relation.cafe_id': {
            data: cafes,
          },
        }}
      />
    </div>
  )
}
