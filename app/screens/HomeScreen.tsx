import React, { useState, useCallback, useEffect } from 'react';
import { Button, View, Text, Modal, NativeModules, NativeEventEmitter, SafeAreaView, FlatList, StyleSheet, Pressable, Alert } from 'react-native';
import { getSyncDeviceInfo, getAsyncDeviceInfo } from '../services/GetDeviceInfo';
import { PermissionsAndroid } from 'react-native';
import WifiManager from 'react-native-wifi-reborn';
import NetInfo from "@react-native-community/netinfo";
import BleManager, { BleScanCallbackType, BleScanMatchMode, BleScanMode, Peripheral } from 'react-native-ble-manager';
import { InstalledApps } from 'react-native-launcher-kit';
import Geolocation from '@react-native-community/geolocation';
import { getBssids } from '../services/GetBssids';
import { getResources } from '../services/Resources';

import { applicationStore } from '../store/applicationStore';
import { Resource } from '../types/Resource';

const BleManagerModule = NativeModules.BleManager;
const bleManagerEmitter = new NativeEventEmitter(BleManagerModule);

const SERVICE_UUIDS: string[] = [];
const SECONDS_TO_SCAN = 3;
const ALLOW_DUPLICATES = true;

const HomeScreen = ({ navigation }) => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [requestedInfo, setRequestedInfo] = useState('');
  const [locationGranted, setLocationGranted] = useState('');
  const [bleDevices, setBleDevices] = useState(new Map<Peripheral['id'], Peripheral>());
  const [resources, setResources] = useState<Resource[]>([]);

  const [isGettingResources, setIsGettingResources] = useState(false);
  const [isLoadingDeviceInfo, setIsLoadingDeviceInfo] = useState(false);
  const [isLoadingApInfo, setIsLoadingApInfo] = useState(false);
  const [isLoadingDeviceNetworkInfo, setIsLoadingDeviceNetworkInfo] = useState(false);
  const [isScanningBleDevices, setIsScanningBleDevices] = useState(false);
  const [isGettingInstalledApps, setIsGettingInstalledApps] = useState(false);
  const [isGettingCurrentLocation, setIsGettingCurrentLocation] = useState(false);
  const bssids = applicationStore.useState(s => s.desiredBSSIDs);

  const token = applicationStore.useState(s => s.userToken);

  const getAvailableResources = useCallback(async () => {
    setIsGettingResources(true);
    const availableResources = await getResources(token);
    setIsGettingResources(false);
    setResources(availableResources.resources);
  }, [resources]);

  useEffect(() => {
    if (resources.length === 0) getAvailableResources();
  }, [resources])

  useEffect(() => {
    /**
     * required for reading list of APs
     */
    PermissionsAndroid.requestMultiple([
      PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
      PermissionsAndroid.PERMISSIONS.ACCESS_BACKGROUND_LOCATION,
      PermissionsAndroid.PERMISSIONS.BLUETOOTH_SCAN,
      PermissionsAndroid.PERMISSIONS.BLUETOOTH_ADVERTISE,
      PermissionsAndroid.PERMISSIONS.BLUETOOTH_CONNECT,
    ]).then(result => {
      if (result['android.permission.ACCESS_FINE_LOCATION'] &&
        result['android.permission.ACCESS_BACKGROUND_LOCATION'] &&
        result['android.permission.BLUETOOTH_SCAN'] &&
        result['android.permission.BLUETOOTH_ADVERTISE'] &&
        result['android.permission.BLUETOOTH_CONNECT'] === 'granted') {
        setLocationGranted('ALLOW');
      }
    }).catch(err => {
      console.log(err)
    });
  }, [locationGranted]);

  const addOrUpdateBleDevice = (id: string, updatedBleDevice: Peripheral) => {
    setBleDevices(map => new Map(map.set(id, updatedBleDevice)))
  };

  const handleDiscoverBleDevices = (bleDevice: Peripheral) => {
    console.log("New Ble Device", bleDevice);
    if (!bleDevice.name) {
      bleDevice.name = 'NO NAME';
    }
    addOrUpdateBleDevice(bleDevice.id, bleDevice);
  };

  const handleStopScan = () => {
    setIsScanningBleDevices(false);
    console.log('Stopped scanning Ble devices');
  };

  useEffect(() => {
    try {
      BleManager.start({ showAlert: false })
        .then(() => console.log("BleManager started"))
        .catch(error => console.error("BleManager could not start", error))
    } catch (error) {
      console.error("Exception thrown when starting BleManager", error)
      return;
    }

    const listeners = [
      bleManagerEmitter.addListener(
        'BleManagerDiscoverPeripheral',
        handleDiscoverBleDevices
      ),
      bleManagerEmitter.addListener(
        'BleManagerStopScan',
        handleStopScan
      )
    ];

    return () => {
      for (const listener of listeners) listener.remove();
    }
  }, []);

  const startBleScan = () => {
    if (!isScanningBleDevices) {
      setBleDevices(new Map<Peripheral['id'], Peripheral>());

      try {
        setIsScanningBleDevices(true);
        BleManager.scan(SERVICE_UUIDS, SECONDS_TO_SCAN, ALLOW_DUPLICATES, {
          matchMode: BleScanMatchMode.Sticky,
          scanMode: BleScanMode.LowLatency,
          callbackType: BleScanCallbackType.AllMatches,
        }).then(() => {
          console.log("Scan promise returned successfully");
        }).catch(err => console.error("Scan promise error", err));
      } catch (error) {
        console.error("Scan exception", error);
      }
    }
  };

  const getDeviceInfo = useCallback(() => {
    setIsLoadingDeviceInfo(true);
    const syncDeviceInfo = getSyncDeviceInfo();
    getAsyncDeviceInfo().then(result => {
      const asyncDeviceInfo = {
        'availableApplicationProviders': result[0],
        'buildId': result[1],
        'batteryLevel': result[2],
        'carrier': result[3],
        'deviceName': result[4],
        'firstInstallTime': result[5],
        'fontScale': result[6],
        'freeDiskStorage': result[7],
        'installerPackageName': result[8],
        'macAddress': result[9],
        'manufacturer': result[10],
        'powerState': result[11],
        'totalDiskCapacity': result[12],
        'totalMemory': result[13],
        'uniqueId': result[14],
        'usedMemory': result[15],
        'userAgent': result[16],
        'batteryCharging': result[17],
        'emulator': result[18],
        'landscape': result[19],
        'locationEnabled': result[20],
        'headphonesConnected': result[21],
        'pinOrFingerprintSet': result[22]
      };
      setRequestedInfo(JSON.stringify({ ...syncDeviceInfo, ...asyncDeviceInfo }));
      setIsModalVisible(true);
    }).catch(error => {
      console.error(error);
    }).finally(() => {
      setIsLoadingDeviceInfo(false);
    });
  }, [requestedInfo]);

  const getApInfo = useCallback(() => {
    setIsLoadingApInfo(true);
    WifiManager.reScanAndLoadWifiList().then(result => {
      setRequestedInfo(JSON.stringify(result));
    }).catch(error => {
      console.error(error);
    }).finally(() => {
      setIsLoadingApInfo(false);
      setIsModalVisible(true);
    });
  }, [requestedInfo]);

  const getDeviceNetworkInfo = useCallback(() => {
    setIsLoadingDeviceNetworkInfo(true);
    NetInfo.fetch().then(result => {
      setRequestedInfo(JSON.stringify(result));
    }).finally(() => {
      setIsLoadingDeviceNetworkInfo(false);
      setIsModalVisible(true);
    });
  }, [requestedInfo]);

  const getInstalledApps = useCallback(() => {
    setIsGettingInstalledApps(true);
    const allInstalledApps = InstalledApps.getSortedApps();
    const installedApps = allInstalledApps.map(ia => ({ 'packageName': ia.packageName, 'appName': ia.label }))
    setRequestedInfo(JSON.stringify(installedApps));
    setIsGettingInstalledApps(false);
    setIsModalVisible(true);
  }, [requestedInfo]);

  const getCurrentLocation = useCallback(() => {
    setIsGettingCurrentLocation(true);
    Geolocation.getCurrentPosition(info => {
      setRequestedInfo(JSON.stringify(info));
      setIsGettingCurrentLocation(false);
      setIsModalVisible(true);
    });
  }, [requestedInfo]);

  const handleItemPress = () => {
    console.log("Item pressed");
  }

  const handleLogout = () => {
    applicationStore.update(applicationState => {
      applicationState.userToken = undefined;
    });
  }

  return (
    <SafeAreaView style={styles.safeAreaViewContainer}>
      {resources.length !== 0 ? (
        <>
          <View style={styles.documentListContainer}>
            <FlatList data={resources} renderItem={({ item }) => (
              <Pressable style={({ pressed }) => pressed ? styles.documentItemContainerPressed : styles.documentItemContainer} onPress={handleItemPress} >
                <Text style={{ fontSize: 20 }}>{item.resourceName}</Text>
                <Text>{item.resourceID}</Text>
              </Pressable>
            )} />
          </View>
          <View style={styles.logoutView}>
            <Button title="Logout" onPress={() => Alert.alert('Logout', 'Are you readdy to logout?', [{ text: 'No', style: 'default' }, { text: 'Yes', style: 'destructive', onPress: handleLogout }])} />
          </View>
        </>
      ) : (
        <>
          <View><Text>Loading Resources</Text></View>
        </>
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeAreaViewContainer: {
    flex: 1,
    padding: 10,
  },
  documentListContainer: {
    flex: 1,
    flexDirection: "column",
  },
  documentItemContainer: {
    flex: 1,
    backgroundColor: "#dedede",
    padding: 10,
    margin: 5
  },
  documentItemContainerPressed: {
    flex: 1,
    backgroundColor: "#dedede",
    padding: 10,
    margin: 5,
    opacity: 0.5
  },
  logoutView: {
    flex: 0,
  }
});

export default HomeScreen;