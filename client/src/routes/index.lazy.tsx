import React from 'react'
import { createLazyFileRoute } from '@tanstack/react-router'
import { Typography } from '@mui/material'

export const Route = createLazyFileRoute('/')({
  component: Index,
})

function Index() {
  return (
    <div className="p-1">
      <Typography variant="h3" >Welcome to the Café Employee manager!</Typography>
    </div>
  )
}