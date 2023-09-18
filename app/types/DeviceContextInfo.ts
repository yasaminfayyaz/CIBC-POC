import { AccessPointItem } from './AccessPointItem';
import { CurrentLocation } from './CurrentLocation';
import { DeviceInfo } from './DeviceInfo';
import { DeviceNetworkInfo } from './DeviceNetworkInfo';
import { InstalledAppItem } from './InstalledAppItem';
import { Peripheral } from 'react-native-ble-manager';

/**
 * Defines an object that represents the collected context information.
 */
export interface DeviceContextInfo {
    accessPoints: Array<AccessPointItem>;
    currentLocation: CurrentLocation;
    deviceInfo: DeviceInfo;
    deviceNetworkInfo: DeviceNetworkInfo;
    bluetoothDevices: Array<Peripheral>;
    installedApps: Array<InstalledAppItem>;
}