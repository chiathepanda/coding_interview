import * as Yup from 'yup';

export const employeeSchema = Yup.object().shape({
  name: Yup.string()
    .min(6, 'Name must be at least 6 characters')
    .max(10, 'Name must be at most 10 characters')
    .required('Name is required'),
  email_address: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  phone_number: Yup.string()
    .matches(/^[89][0-9]{7}$/, 'The Phone Number must start with either 8 or 9 and must have 8 digits in total.')
    .required('Phone number is required'),
  gender: Yup.string()
    .oneOf(['male', 'female'], 'Gender is required')
    .required(),
  cafe_relation: Yup.object().shape({
    start_date: Yup.string()
      .matches(
        /^\d{4}-\d{2}-\d{2}$/,
        'Date must be in the format YYYY-MM-DD'
      ),
    cafe_id: Yup.string().nullable().when('start_date', {
      is: (start_date) => !!start_date,
      then: (schema) => schema.required('Cafe ID is required when Start Date is filled'),
      otherwise: (schema) => schema.nullable(),
    }),
  }),
});
