import React, { useMemo, useRef, useEffect } from 'react';
import { Field, ErrorMessage, } from 'formik';

import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';

import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs from 'dayjs';


const renderFields = (setFieldValue, handleChange, handleBlur, values, fieldConfigs, dropdownFieldValues?) => {

    return fieldConfigs.map((field) => {
        let value = null
        let field_name = ""
        if (field.name.includes('.')) {
            const [parent, child] = field.name.split('.');
            value = values[parent][child] || "";
            field_name = parent + '.' + child
        }
        else {
            value = values[field.name]
            field_name = field.name
        }
        // Conditional rendering for dropdown fields
        if (field.type === 'dropdown') {
            return (
                <div key={field_name} style={{ marginBottom: 16 }}>
                    <Field
                        name={field_name}
                        as={TextField}
                        select
                        margin="dense"
                        label={field.label}
                        fullWidth
                        value={value || ""}
                        onChange={handleChange}
                        onBlur={handleBlur}
                    >
                        <MenuItem key="" value="">
                            Select a {field.label}
                        </MenuItem>
                        {field.options.map((option) => (
                            <MenuItem key={option.value} value={option.value}>
                                {option.label}
                            </MenuItem>
                        ))}
                    </Field>
                    <ErrorMessage name={field_name} component="div" className="error" />
                </div>
            );
        }

        if (field.type == 'date') {
            return (
                <div key={field_name} style={{ marginBottom: 16 }}>
                    <Field
                        name={field_name}
                        as={DatePicker}
                        margin="dense"
                        label={field.label}
                        fullWidth
                        inputProps={field.inputProps}
                        value={value == "" ? null : dayjs(value)}
                        onChange={(newDate) =>
                            setFieldValue(field_name, newDate ? newDate.format("YYYY-MM-DD") : null)
                        }
                        format="YYYY-MM-DD"
                    />
                    <ErrorMessage name={field_name} component="div" className="error" />
                </div>
            );
        }

        // Default case: Render a normal TextField
        return (
            <div key={field_name} style={{ marginBottom: 16 }}>
                <Field
                    name={field_name}
                    as={TextField}
                    margin="dense"
                    label={field.label}
                    fullWidth
                    inputProps={field.inputProps}
                    value={value}
                    onChange={handleChange}
                />
                <ErrorMessage name={field_name} component="div" className="error" />
            </div>
        );
    });
};

export default renderFields;
