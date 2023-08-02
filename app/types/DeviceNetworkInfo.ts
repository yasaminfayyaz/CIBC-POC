export interface DeviceNetworkInfoDetails {
    bssid: string;
    frequency: number;
    ipAddress: string;
    isConnectionExpensive: boolean;
    linkSpeed: number;
    rxLinkSpeed: number;
    ssid: string;
    strength: number;
    subnet: string;
    txLinkSpeed: number;
}

export interface DeviceNetworkInfo {
    details: DeviceNetworkInfoDetails;
    isConnected: boolean;
    isInternetReachable: boolean;
    isWifiEnabled: boolean;
    type: string;
}