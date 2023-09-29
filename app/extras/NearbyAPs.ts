import {useState, useEffect, useCallback} from 'react';
import { PermissionsAndroid } from 'react-native';
import WifiManager from 'react-native-wifi-reborn';

const [apInfo, setApInfo] = useState('');
const [locationGranted, setLocationGranted] = useState('');

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

const getApInfo = useCallback(() => {
    WifiManager.reScanAndLoadWifiList().then(result => {
        setApInfo(JSON.stringify(result));
    }).catch(error => {
      console.error(error);
    }).finally(() => {
    });
  }, [apInfo]);