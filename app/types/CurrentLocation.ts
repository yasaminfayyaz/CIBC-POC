/**
 * Helper definition for user coordinates.
 * Includes accuracy, altitude, heading, latitude, longitude, and speed.
 */
export interface CurrentLocationCoords {
    accuracy: number;
    altitude: number;
    heading: number;
    latitude: number;
    longitude: number;
    speed: number;
}

/**
 * Helper definition for connection location extras.
 * This only includes the type of network location.
 */
export interface CurrentLocationExtras {
    networkLocationType: string;
}

/**
 * Defines an object that represents the user's current location.
 */
export interface CurrentLocation {
    coords: CurrentLocationCoords;
    extras: CurrentLocationExtras;
    mocked: boolean;
    timestamp: number;
}