import { useQuery } from '@tanstack/react-query';
import { fetchCafes } from '../../api/cafes';

export const useFetchCafes = (enabled = true) => {
    return useQuery({
        queryKey: ['cafes'],
        queryFn: fetchCafes,
        enabled: enabled,
    });
};