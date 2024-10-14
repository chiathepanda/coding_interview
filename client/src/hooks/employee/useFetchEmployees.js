import { useQuery } from '@tanstack/react-query';
import { fetchEmployees } from '../../api/employees';

export const useFetchEmployees = (enabled = true) => {
    return useQuery({
        queryKey: ['employees'],
        queryFn: fetchEmployees,
        enabled: enabled,
    });
};