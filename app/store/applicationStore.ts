import { Store } from 'pullstate';
import { DeviceContextInfo } from '../types/DeviceContextInfo';

interface UIStore {
    userToken?: string;
    deviceContextInfo?: DeviceContextInfo;
}

export const applicationStore = new Store<UIStore>({ userToken: undefined, deviceContextInfo: undefined });