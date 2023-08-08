export interface LocationProvider {
    fused: boolean;
    network: boolean;
    gps: boolean;
    passive: boolean;
}

export interface PowerState {
    lowPowerMode: boolean;
    batteryLevel: number;
    batteryState: string;
}

export interface DeviceInfo {
    applicationName: string;
    brand: string;
    // buildNumber: string;
    // bundleId: string;
    // deviceId: string;
    // deviceType: string;
    // readableVersion: string;
    systemName: string;
    // systemVersion: string;
    // version: string;
    // deviceHasNotch: boolean;
    // deviceHasDynamicIsland: boolean;
    // tablet: boolean;
    availableLocationProviders: LocationProvider;
    // buildId: string;
    // batteryLevel: number;
    // carrier: string;
    // deviceName: string;
    firstInstallTime: number; // in milliseconds
    // fontScale: number;
    // freeDiskStorage: number;
    // installerPackageName: string;
    macAddress: string;
    // manufacturer: string;
    // powerState: PowerState;
    // totalDiskCapacity: number;
    // totalMemory: number;
    uniqueId: string;
    // usedMemory: number;
    // userAgent: string;
    // batteryCharging: boolean;
    emulator: boolean;
    // landscape: boolean;
    locationEnabled: boolean;
    // headphonesConnected: boolean;
    pinOrFingerprintSet: boolean;
}