import React, { useState, useCallback, useEffect } from 'react';
import { Button, View } from 'react-native';
import { getSyncDeviceInfo, getAsyncDeviceInfo } from '../services/GetDeviceInfo';
import { PermissionsAndroid } from 'react-native';
import WifiManager from 'react-native-wifi-reborn';

const HomeScreen = ({ navigation }) => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [deviceInfo, setDeviceInfo] = useState();
  const [wifiInfo, setWifiInfo] = useState();
  const [locationGranted, setLocationGranted] = useState('');
  const [isLoadingWifiInfo, setIsLoadingWifiInfo] = useState(false);

  useEffect(() => {
    /**
     * required for reading list of APs
     */
    PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
      {
        title: 'Location permission is required for WiFi connections',
        message: 'This app needs location permission as this is required to scan for wifi networks.',
        buttonNegative: 'DENY',
        buttonPositive: 'ALLOW'
      }
    ).then(result => {
      setLocationGranted(result);
    });
  }, [locationGranted]);

  const getDeviceInfo = useCallback(() => {
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
        'ipAddress': result[8],
        'installerPackageName': result[9],
        'macAddress': result[10],
        'manufacturer': result[11],
        'powerState': result[12],
        'totalDiskCapacity': result[13],
        'totalMemory': result[14],
        'uniqueId': result[15],
        'usedMemory': result[16],
        'userAgent': result[17],
        'batteryCharging': result[18],
        'emulator': result[19],
        'landscape': result[20],
        'locationEnabled': result[21],
        'headphonesConnected': result[22],
        'pinOrFingerprintSet': result[23]
      };
      setDeviceInfo({ ...syncDeviceInfo, ...asyncDeviceInfo });
    }).catch(error => {
      console.error(error);
    });
  }, [deviceInfo]);

  const getWifiInfo = useCallback(() => {
    setIsLoadingWifiInfo(true);
    WifiManager.reScanAndLoadWifiList().then(result => {
      setWifiInfo(result);
    }).catch(error => {
      console.error(error);
    }).finally(() => {
      setIsLoadingWifiInfo(false);
    });
  }, [wifiInfo]);

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Button title="Get Device Info" onPress={getDeviceInfo} />
      <Button title="Get WiFi Info" onPress={getWifiInfo} disabled={isLoadingWifiInfo} />
    </View>
  );
};

export default HomeScreen;