/**
 * Import required packages
 */
import { Store } from 'pullstate';
import { DeviceContextInfo } from '../types/DeviceContextInfo';
import { BSSID } from '../types/BSSID';

/**
 * Define an object that represents data to be available globally within the application.
 * Fields can be included or removed as needed.
 */
interface UIStore {
    userToken?: string;
    deviceContextInfo?: DeviceContextInfo;
    desiredBSSIDs?: Array<BSSID>;
}

/**
 * Creates and exports (makes available) the application store.
 */
export const applicationStore = new Store<UIStore>({ userToken: undefined, deviceContextInfo: undefined, desiredBSSIDs: undefined });