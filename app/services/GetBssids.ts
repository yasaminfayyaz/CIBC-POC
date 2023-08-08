import { BASE_URL } from '../constants/BaseUrl';
import { BSSID } from '../types/BSSID';

export const getBssids = async (): Promise<Array<BSSID>> => {
    const getBssidsPromise = await fetch(`${BASE_URL}/get_bssids`, {
        method: 'get'
    });
    const bssids: Promise<Array<BSSID>> = await getBssidsPromise.json();
    return bssids;
}