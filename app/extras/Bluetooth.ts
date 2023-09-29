import {useState, useEffect} from 'react';
import {NativeModules, NativeEventEmitter} from 'react-native';
import BleManager, { BleScanCallbackType, BleScanMatchMode, BleScanMode, Peripheral } from 'react-native-ble-manager';

const SERVICE_UUIDS: string[] = [];
const SECONDS_TO_SCAN = 3;
const ALLOW_DUPLICATES = true;

const [bleDevices, setBleDevices] = useState(new Map<Peripheral['id'], Peripheral>());
const [isScanningBleDevices, setIsScanningBleDevices] = useState(false);

const BleManagerModule = NativeModules.BleManager;
const bleManagerEmitter = new NativeEventEmitter(BleManagerModule);

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