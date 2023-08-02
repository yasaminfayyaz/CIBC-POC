export interface CurrentLocationCoords {
    accuracy: number;
    altitude: number;
    heading: number;
    latitude: number;
    longitude: number;
    speed: number;
}

export interface CurrentLocationExtras {
    networkLocationType: string;
}

export interface CurrentLocation {
    coords: CurrentLocationCoords;
    extras: CurrentLocationExtras;
    mocked: boolean;
    timestamp: number;
}