/**
 * Defines a helper object that represents detailed device networking information.
 * Additional data that is not being used is commented out.
 */
export interface DeviceNetworkInfoDetails {
    bssid: string; // of the current network
    // frequency: number;
    ipAddress: string; // promisingly external
    // isConnectionExpensive: boolean;
    // linkSpeed: number;
    // rxLinkSpeed: number;
    // ssid: string;
    strength: number; //in percentage
    // subnet: string;
    // txLinkSpeed: number;
}

/**
 * Defines an object that represents the device's networking information.
 * Additional data that is not being used is commented out.
 */
export interface DeviceNetworkInfo {
    details: DeviceNetworkInfoDetails;
    isConnected: boolean;
    // isInternetReachable: boolean;
    // isWifiEnabled: boolean;
    type: string;
}