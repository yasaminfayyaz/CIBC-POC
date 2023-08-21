import { BASE_URL } from '../constants/BaseUrl';
import { GetResourceAPIReturn } from '../types/Resource';

export const getResources = async (token?: string): Promise<GetResourceAPIReturn> => {

    const response = await fetch(`${BASE_URL}/get_resources`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        method: 'GET'
    });

    const responseBody = await response.json();

    return responseBody;
};