/**
 * Import required packages.
 */
import { BASE_URL } from '../constants/BaseUrl';
import { APIResponse } from '../types/APIResponse';

/**
 * 
 * @param username Username used by the employee (employeeID)
 * @param password Password used by the employee
 * @returns Returns an API Response object containing an authorization token if successful, or an error message otherwise.
 */
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

/**
 * 
 * @param username Username used by the employee (employeeID)
 * @param oldPassword Old password used by the employee
 * @param newPassword New password to be used by the employee
 * @returns Returns an API Response object containing a code and message regarding the successfulness of the operation.
 */
export const setPassword = async (username: string, oldPassword: string, newPassword: string): Promise<APIResponse> => {
    const response = await fetch(`${BASE_URL}/set_password`, {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({ 'employeeID': username, 'oldPassword': oldPassword, 'newPassword': newPassword }),
    });

    const responseBody = await response.json();
    return responseBody;
};