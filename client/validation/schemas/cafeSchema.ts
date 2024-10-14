import * as Yup from 'yup';

const MAX_FILE_SIZE = import.meta.env.VITE_MAX_FILE_SIZE;

export const cafeSchema = Yup.object().shape({
  name: Yup.string()
    .min(6, 'Name must be at least 6 characters')
    .max(10, 'Name must be at most 10 characters')
    .required('Name is required'),
  description: Yup.string().required('Max 256 chars.').required(),
  logo: Yup.mixed()
    .nullable()
    .test(
      'fileSize',
      `The file uploaded is too large. The maximum limit is ${MAX_FILE_SIZE / 1024 / 1024} MB.`,
      (value) => {
        if (!value) return true;
        // Check if there is a file and if its size is valid
        return value && value.size <= MAX_FILE_SIZE;
      }
    ).test(
      'fileType',
      'The uploaded file must be an image (e.g., PNG, JPEG).',
      (value) => {
        if (!value) return true; // If no file is uploaded, it's valid
        return value && value.type.startsWith('image/');
      }
    ),
  location: Yup.string().required(),
});