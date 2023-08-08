import { Store } from 'pullstate';
import { DeviceContextInfo } from '../types/DeviceContextInfo';
import { BSSID } from '../types/BSSID';

interface UIStore {
    userToken?: string;
    deviceContextInfo?: DeviceContextInfo;
    desiredBSSIDs?: Array<BSSID>;
}

export const applicationStore = new Store<UIStore>({ userToken: undefined, deviceContextInfo: undefined, desiredBSSIDs: undefined });