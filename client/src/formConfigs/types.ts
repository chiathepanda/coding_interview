export type FieldType = 'text' | 'email' | 'dropdown' | 'date';

export interface Option {
    value: string | number | null;
    label: string;
}

export interface FieldConfig {
    name: string;
    label: string;
    type: FieldType;
    inputProps?: { maxLength: number };
    dynamic?: boolean;
    options?: Option[];
}
