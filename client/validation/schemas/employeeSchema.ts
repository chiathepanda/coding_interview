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
    .required("Gender is required"),
  cafe_relation: Yup.object().shape({
    cafe_id: Yup.string().nullable(),
    start_date: Yup.string()
      .nullable()
      .test('start-date-conditional', 'Start date must be filled when Cafe is filled', function (value) {
        const { cafe_id, start_date } = this.parent;
        if ((cafe_id == null && start_date == null) || (cafe_id && start_date)) {
          return true;
        }
        return false;
      }),
  }),
});
