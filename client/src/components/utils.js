export function flattenKeys(obj, parent = '', res = {}) {
    for (const [key, value] of Object.entries(obj)) {
        const propName = parent ? `${parent}.${key}` : key;

        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
            flattenKeys(value, propName, res);
        } else {
            res[propName] = value;
        }
    }
    return res;
};

// e.g. 
// {'a.b': val, 
//     {'a': 
//         {'b': val}},
//     'a.c': val2}

// {'a': 
//     {'b': val, 
//     'c': val2} }
export function unflattenKeysToNested(obj) {
    let result = {};

    Object.keys(obj).forEach(key => {
        if (key.includes('.')) {
            const [parent, child] = key.split('.');

            if (!result[parent]) {
                result[parent] = {};
            }

            // Assign the value to the child key under the parent
            if (obj[parent] && obj[parent][child]) {
                result[parent][child] = obj[parent][child];
            } else {
                result[parent][child] = obj[key]
            }

        } else {
            // If no dot is found, assign the key-value pair directly to result
            if (!result[key]) {
                result[key] = obj[key];
            }

        }
    });

    return result;
}