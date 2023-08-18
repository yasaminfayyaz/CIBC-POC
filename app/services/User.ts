import { BASE_URL } from '../constants/BaseUrl';
import { APIResponse } from '../types/APIResponse';

export const login = async (username: string, password: string): Promise<APIResponse> => {
    const response = await fetch(`${BASE_URL}/login`, {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({ "employeeID": username, "password": password })
    });

    const responseBody = await response.json();
    return responseBody;
};

export const setPassword = async (token: string, oldPassword: string, newPassword: string): Promise<APIResponse> => {
    const response = await fetch(`${BASE_URL}/set_password`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        method: 'POST',
        body: JSON.stringify({ 'oldPassword': oldPassword, 'newPassword': newPassword }),
    });

    const responseBody = await response.json();
    return responseBody;
};