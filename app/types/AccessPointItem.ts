/**
 * Defines an object type that represents an Access Point.
 * Some properties are not used because they were not used.
 */
export interface AccessPointItem {
    // timestamp: number;
    level: number;
    // frequency: number;
    capabilities: string;
    BSSID: string;
    // SSID: string;
}