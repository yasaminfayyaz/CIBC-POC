import React, { useState, useCallback, useEffect } from 'react';
import { Button, View, Text, Modal, NativeModules, NativeEventEmitter } from 'react-native';
import { getSyncDeviceInfo, getAsyncDeviceInfo } from '../services/GetDeviceInfo';
import { PermissionsAndroid } from 'react-native';
import WifiManager from 'react-native-wifi-reborn';
import NetInfo from "@react-native-community/netinfo";
import BleManager, { BleScanCallbackType, BleScanMatchMode, BleScanMode, Peripheral } from 'react-native-ble-manager';

const BleManagerModule = NativeModules.BleManager;
const bleManagerEmitter = new NativeEventEmitter(BleManagerModule);

const SERVICE_UUIDS: string[] = [];
const SECONDS_TO_SCAN = 5;
const ALLOW_DUPLICATES = true;

const HomeScreen = ({ navigation }) => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [requestedInfo, setRequestedInfo] = useState('');
  const [locationGranted, setLocationGranted] = useState('');
  const [bleDevices, setBleDevices] = useState(new Map<Peripheral['id'], Peripheral>());

  const [isLoadingDeviceInfo, setIsLoadingDeviceInfo] = useState(false);
  const [isLoadingApInfo, setIsLoadingApInfo] = useState(false);
  const [isLoadingDeviceNetworkInfo, setIsLoadingDeviceNetworkInfo] = useState(false);
  const [isScanningBleDevices, setIsScanningBleDevices] = useState(false);

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
      BleManager.start({showAlert: false})
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
  
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Modal
        animationType='fade'
        visible={isModalVisible}
        onRequestClose={() => {
          setIsModalVisible(false);
        }}
      >
        <View style={{ flex: 1, alignItems: 'center', alignContent: 'center' }}>
          <Text>{requestedInfo}</Text>
          <Button title="Close" onPress={() => setIsModalVisible(false)} />
        </View>
      </Modal>
      <Button title="Get Device Info" onPress={getDeviceInfo} disabled={isLoadingDeviceInfo} />
      <Button title="Get AP Info" onPress={getApInfo} disabled={isLoadingApInfo} />
      <Button title="Get Device Network Info" onPress={getDeviceNetworkInfo} disabled={isLoadingDeviceNetworkInfo} />
      <Button title="Get Bluetooth Info" onPress={startBleScan} disabled={isScanningBleDevices} />
    </View>
  );
};

export default HomeScreen;