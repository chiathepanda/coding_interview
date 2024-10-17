export const fetchEmployees = async (params) => {

    let url = params['queryKey'].length > 1
        ? `${import.meta.env.VITE_API_URL}/employees?cafe_id=${params['queryKey'][1]['cafe_id']}`
        : `${import.meta.env.VITE_API_URL}/employees`;

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error('Failed to fetch employees');
    }

    return response.json();
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
    // cafe_relation.cafe_id needs to be correct; not the cafe_relation.cafe_name

    const response = await fetch(`${import.meta.env.VITE_API_URL}/employee`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedEmployee),
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

    return response;
};