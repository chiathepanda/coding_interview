import { unflattenKeysToNested } from "../components/utils";

export const fetchEmployees = async () => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/employees`);

    if (!response.ok) {
        throw new Error('Failed to fetch employees');
    }

    const data = await response.json();

    return data.map((employee) => ({
        ...employee,
        // cafe: employee.cafe.name,
    }));
};

export const addEmployee = async (employee) => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/employee`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(employee),
    });

    if (!response.ok) {
        throw new Error('Failed to add employee');
    }

    return response.json();
};

export const editEmployee = async (updatedEmployee) => {
    const nestedupdatedEmployee = unflattenKeysToNested(updatedEmployee)

    const response = await fetch(`${import.meta.env.VITE_API_URL}/employee`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(nestedupdatedEmployee),
    });

    if (!response.ok) {
        throw new Error('Failed to edit employee');
    }

    return response.json();
};

export const deleteEmployee = async (employeeId) => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/employee`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(employeeId),
    });

    if (!response.ok) {
        throw new Error('Failed to delete employee');
    }

    return response.json();
};