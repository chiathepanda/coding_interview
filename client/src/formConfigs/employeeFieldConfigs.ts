import { FieldConfig } from "./types";

export const employeeFieldConfigs: FieldConfig[] = [
  { name: 'name', label: 'Name', type: 'text' },
  { name: 'email_address', label: 'Email Address', type: 'email' },
  { name: 'phone_number', label: 'Phone Number', type: 'text', inputProps: { maxLength: 8 } },
  {
    name: 'gender', label: 'Gender', type: 'dropdown', dynamic: false,
    options: [
      { value: null, label: '' },
      { value: 'male', label: 'Male' },
      { value: 'female', label: 'Female' },
    ]
  },
  {
    name: 'cafe_relation.cafe_id', label: 'Cafe', type: 'dropdown', dynamic: true, // options list is fetched when focused
  },
  { name: 'cafe_relation.start_date', label: 'Start Date', type: 'date' }
];

