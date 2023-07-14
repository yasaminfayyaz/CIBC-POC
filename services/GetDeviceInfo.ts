import {
    getApplicationName,
    getAvailableLocationProviders,
    getBuildId,
    getBatteryLevel,
    getBrand,
    getBuildNumber,
    getBundleId,
    getCarrier,
    getDeviceId,
    getDeviceType,
    getDeviceName,
    getFirstInstallTime,
    getFontScale,
    getFreeDiskStorage,
    getIpAddress,
    getInstallerPackageName,
    getMacAddress,
    getManufacturer,
    getModel,
    getPowerState,
    getReadableVersion,
    getSystemName,
    getSystemVersion,
    getTotalDiskCapacity,
    getTotalMemory,
    getUniqueId,
    getUsedMemory,
    getUserAgent,
    getVersion,
    hasNotch,
    hasDynamicIsland,
    isBatteryCharging,
    isEmulator,
    isLandscape,
    isLocationEnabled,
    isHeadphonesConnected,
    isPinOrFingerprintSet,
    isTablet,
} from 'react-native-device-info';

export const getSyncDeviceInfo = () => {
    const applicationName = getApplicationName();
    const brand = getBrand();
    const buildNumber = getBuildNumber();
    const bundleId = getBundleId();
    const deviceId = getDeviceId();
    const deviceType = getDeviceType();
    const model = getModel();
    const readableVersion = getReadableVersion();
    const systemName = getSystemName();
    const systemVersion = getSystemVersion();
    const version = getVersion();
    const deviceHasNotch = hasNotch();
    const deviceHasDynamicIsland = hasDynamicIsland();
    const tablet = isTablet();

    return {
        'applicationName': applicationName,
        'brand': brand,
        'buildNumber': buildNumber,
        'bundleId': bundleId,
        'deviceId': deviceId,
        'deviceType': deviceType,
        'model': model,
        'readableVersion': readableVersion,
        'systemName': systemName,
        'systemVersion': systemVersion,
        'version': version,
        'deviceHasNotch': deviceHasNotch,
        'deviceHasDynamicIsland': deviceHasDynamicIsland,
        'tablet': tablet
    };
};

export const getAsyncDeviceInfo = () => {
    const availableApplicationProviders = getAvailableLocationProviders();
    const buildId = getBuildId();
    const batteryLevel = getBatteryLevel();
    const carrier = getCarrier();
    const deviceName = getDeviceName();
    const firstInstallTime = getFirstInstallTime();
    const fontScale = getFontScale();
    const freeDiskStorage = getFreeDiskStorage();
    const ipAddress = getIpAddress();
    const installerPackageName = getInstallerPackageName();
    const macAddress = getMacAddress();
    const manufacturer = getManufacturer();
    const powerState = getPowerState();
    const totalDiskCapacity = getTotalDiskCapacity();
    const totalMemory = getTotalMemory();
    const uniqueId = getUniqueId();
    const usedMemory = getUsedMemory();
    const userAgent = getUserAgent();
    const batteryCharging = isBatteryCharging();
    const emulator = isEmulator();
    const landscape = isLandscape();
    const locationEnabled = isLocationEnabled();
    const headphonesConnected = isHeadphonesConnected();
    const pinOrFingerprintSet = isPinOrFingerprintSet();

    return Promise.all([
        availableApplicationProviders,
        buildId,
        batteryLevel,
        carrier,
        deviceName,
        firstInstallTime,
        fontScale,
        freeDiskStorage,
        ipAddress,
        installerPackageName,
        macAddress,
        manufacturer,
        powerState,
        totalDiskCapacity,
        totalMemory,
        uniqueId,
        usedMemory,
        userAgent,
        batteryCharging,
        emulator,
        landscape,
        locationEnabled,
        headphonesConnected,
        pinOrFingerprintSet
    ]);
};