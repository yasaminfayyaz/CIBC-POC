export interface InstalledApp {
  packageName: string;
}

export interface CurrentLocationCoords {
  latitude: number;
  longitude: number;
}

export interface CurrentLocation {
  mocked: boolean;
}

export interface DeviceInfo {
  uniqueId: string;
  pinOrFingerprintSet: boolean;
  emulator: boolean;
  brand: string;
  firstInstallTime: number;
}

export interface AccessRequest {
  ResourceID: number;
  ActionID: string;
  installedApps: InstalledApp[];
  CurrentLocationCoords: CurrentLocationCoords;
  DeviceInfo: DeviceInfo;
  CurrentLocation: CurrentLocation;
}
