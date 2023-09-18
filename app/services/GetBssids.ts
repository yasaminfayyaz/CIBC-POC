/**
 * Import required packages.
 */
import { BASE_URL } from '../constants/BaseUrl';
import { BSSID } from '../types/BSSID';

/**
 * Defines and exports a function that makes a call to the API.
 * @returns Returns a promise to an array of BSSIDs
 */
export const getBssids = async (): Promise<Array<BSSID>> => {
    const getBssidsPromise = await fetch(`${BASE_URL}/get_bssids`, {
        method: 'get'
    });
    const bssids: Promise<Array<BSSID>> = await getBssidsPromise.json();
    return bssids;
}