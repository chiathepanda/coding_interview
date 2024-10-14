let baseUrl = import.meta.env.VITE_API_URL;

export const fetchCafes = async () => {
    const response = await fetch(`${baseUrl}/cafes`);
    if (!response.ok) {
        throw new Error('Failed to fetch cafes');
    }
    const data = await response.json();

    return data.map((cafe) => ({
        ...cafe,
    }));
};

export const addCafe = async (newCafe) => {
    const formCafe = new FormData();

    if (!newCafe.logo) {
        delete newCafe.logo;
    }

    for (const name in newCafe) {
        formCafe.append(name, newCafe[name]);
    }

    const response = await fetch(`${import.meta.env.VITE_API_URL}/cafe`, {
        method: 'POST',
        body: formCafe,
    });

    if (!response.ok) {
        throw new Error('Failed to add cafe: ' + response.error);
    }

    return response.json();
};

export const editCafe = async (updatedCafe) => {
    const formCafe = new FormData();

    if (!updatedCafe.logo) {
        delete updatedCafe.logo;
    }

    for (const name in updatedCafe) {
        formCafe.append(name, updatedCafe[name]);
    }

    const response = await fetch(`${import.meta.env.VITE_API_URL}/cafe`, {
        method: 'PUT',
        body: formCafe,
    });

    if (!response.ok) {
        if (response.status === 415) {
            throw new Error('Failed to edit cafe. Unsupported Media Type: Please ensure the file format is correct.');
        } else if (response.status === 400) {
            throw new Error('Failed to edit cafe. Bad Request: Please ensure all required fields are provided.');
        } else if (response.status === 500) {
            throw new Error('Failed to edit cafe. Server Error: Please try again later.');
        } else {
            throw new Error('Failed to edit cafe: ' + response.statusText);
        }
    }
    return response.json();
};

export const deleteCafe = async (cafeId) => {
    const formCafe = new FormData();
    formCafe.append("id", cafeId)

    const response = await fetch(`${import.meta.env.VITE_API_URL}/cafe`, {
        method: 'DELETE',
        body: formCafe,
    });
    if (!response.ok) {
        throw new Error('Failed to delete cafe');
    }

    // Check if the response status is 204 (No Content) or if the body is empty
    if (response.status === 204 || response.headers.get('content-length') === '0') {
        return;
    }

    return response;
};