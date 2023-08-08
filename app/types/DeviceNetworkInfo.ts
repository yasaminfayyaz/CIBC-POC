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

export interface DeviceNetworkInfo {
    details: DeviceNetworkInfoDetails;
    isConnected: boolean;
    // isInternetReachable: boolean;
    // isWifiEnabled: boolean;
    type: string;
}