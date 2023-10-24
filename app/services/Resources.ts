/**
 * Import required packages.
 */
import { BASE_URL } from '../constants/BaseUrl';
import { GetResourceAPIReturn } from '../types/Resource';

/**
 * Defines and exports a function that gets resources from the API.
 * @param token JWT token used to authorize the request and identify the agent.
 * @returns Returns a promise to a list of resources.
 */
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