/**
 * Defines an object type that represents a response from the API.
 * These responses are provided by the PEP.
 */
export interface APIResponse {
    code: number;
    message: string;
    token?: string;
}