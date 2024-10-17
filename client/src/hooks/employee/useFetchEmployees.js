import { useQuery } from '@tanstack/react-query';
import { fetchEmployees } from '../../api/employees';

export const useFetchEmployees = (enabled = true, params) => {
    return useQuery({
        queryKey: params ? ['employees', { "cafe_id": params['cafe_id'] }] : ['employees'],
        queryFn: fetchEmployees,
        enabled: enabled,
    });
};