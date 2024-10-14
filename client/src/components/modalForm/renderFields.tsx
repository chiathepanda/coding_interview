import React, { useMemo } from 'react';
import { Field, ErrorMessage, } from 'formik';

import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';

// import { DateField } from '@mui/x-date-pickers/DateField';
// import { DatePicker } from '@mui/x-date-pickers/DatePicker';
// import dayjs from 'dayjs';

const renderFields = (setFieldValue, handleChange, handleBlur, values, fieldConfigs, dropdownFieldValues?) => {
    return fieldConfigs.map((field) => {
        // Conditional rendering for dropdown fields
        if (field.type === 'dropdown') {
            return (
                <div key={field.name} style={{ marginBottom: 16 }}>
                    <Field
                        name={field.name}
                        as={TextField}
                        select
                        margin="dense"
                        label={field.label}
                        fullWidth
                        value={values[field.name]}
                        onChange={handleChange}
                        onBlur={handleBlur}
                    >
                        {field.options.map((option) => (
                            <MenuItem key={option.value} value={option.value}>
                                {option.label}
                            </MenuItem>
                        ))}
                    </Field>
                    <ErrorMessage name={field.name} component="div" className="error" />
                </div>
            );
        }

        if (field.type == 'date') {
            return (
                <div key={field.name} style={{ marginBottom: 16 }}>
                    <Field
                        name={field.name}
                        as={TextField}
                        margin="dense"
                        label={field.label}
                        fullWidth
                        inputProps={field.inputProps}
                        value={values[field.name]}
                        onChange={(event) => setFieldValue('startDate', event.target.value)}
                        onBlur={handleBlur}
                    />
                    <ErrorMessage name={field.name} component="div" className="error" />
                </div>
            );
        }

        // Default case: Render a normal TextField
        return (
            <div key={field.name} style={{ marginBottom: 16 }}>
                <Field
                    name={field.name}
                    as={TextField}
                    margin="dense"
                    label={field.label}
                    fullWidth
                    inputProps={field.inputProps}
                    value={values[field.name]}
                    onChange={handleChange}
                />
                <ErrorMessage name={field.name} component="div" className="error" />
            </div>
        );
    });
};

export default renderFields;
