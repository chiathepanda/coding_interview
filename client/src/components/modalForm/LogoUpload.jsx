import React, { useState, useCallback, useEffect } from 'react';
import { Box, Button, IconButton } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DeleteIcon from '@mui/icons-material/Delete';
import { styled } from '@mui/material/styles';

const VisuallyHiddenInput = styled('input')({
    clip: 'rect(0 0 0 0)',
    clipPath: 'inset(50%)',
    height: 1,
    overflow: 'hidden',
    position: 'absolute',
    bottom: 0,
    left: 0,
    whiteSpace: 'nowrap',
    width: 1,
});

const LogoUpload = ({ name, filePreview, setFilePreview, setFieldValue }) => {
    const previewFileUpload = useCallback((event) => {
        const reader = new FileReader();
        const file = event.target.files[0];
        reader.onloadend = () => {
            setFilePreview(reader.result);
        };
        reader.readAsDataURL(file);
    }, [setFilePreview]);

    const previewRemove = useCallback(() => {
        setFilePreview("");
        setFieldValue(name, null);
    }, [setFilePreview, setFieldValue]);

    // useEffect(() => {
    //     if (initialFile) {
    //         setFilePreview(initialFile);
    //     }
    // }, [initialFile, setFilePreview]);

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
            {filePreview && (
                <Box
                    component="img"
                    src={filePreview}
                    alt="Logo preview"
                    sx={{ maxWidth: '100%', maxHeight: 120 }}
                />
            )}
            {filePreview && (
                <div>
                    <IconButton color="error" onClick={previewRemove}>
                        <DeleteIcon />
                    </IconButton>
                </div>
            )}
            <Button
                component="label"
                role={undefined}
                variant="contained"
                tabIndex={-1}
                startIcon={<CloudUploadIcon />}
            >
                Upload files
                <VisuallyHiddenInput
                    type="file"
                    onChange={(event) => {
                        if (!event.target.files) return;
                        setFieldValue(name, event.target.files[0]);
                        previewFileUpload(event);
                    }}
                />
            </Button>


        </div>
    );
};

export default LogoUpload;
