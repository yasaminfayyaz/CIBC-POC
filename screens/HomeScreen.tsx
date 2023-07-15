import React, { useState, useCallback, useEffect } from 'react';
import { Alert, Button, View, Text, Modal } from 'react-native';
import { getSyncDeviceInfo, getAsyncDeviceInfo } from '../services/GetDeviceInfo';
import { PermissionsAndroid } from 'react-native';
import WifiManager from 'react-native-wifi-reborn';

const HomeScreen = ({ navigation }) => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  // const [deviceInfo, setDeviceInfo] = useState({});
  // const [wifiInfo, setWifiInfo] = useState([]);
  const [requestedInfo, setRequestedInfo] = useState('');
  const [locationGranted, setLocationGranted] = useState('');
  const [isLoadingDeviceInfo, setIsLoadingDeviceInfo] = useState(false);
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
      setRequestedInfo(JSON.stringify({ ...syncDeviceInfo, ...asyncDeviceInfo }));
      setIsModalVisible(true);
    }).catch(error => {
      console.error(error);
    }).finally(() => {
      setIsLoadingDeviceInfo(false);
    });
  }, [requestedInfo]);

  const getWifiInfo = useCallback(() => {
    setIsLoadingWifiInfo(true);
    WifiManager.reScanAndLoadWifiList().then(result => {
      setRequestedInfo(JSON.stringify(result));
    }).catch(error => {
      console.error(error);
    }).finally(() => {
      setIsLoadingWifiInfo(false);
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
        <View style={{flex: 1, alignItems: 'center', alignContent: 'center'}}>
          <Text>{requestedInfo}</Text>
          <Button title="Close" onPress={() => setIsModalVisible(false)} />
        </View>
      </Modal>
      <Button title="Get Device Info" onPress={getDeviceInfo} disabled={isLoadingDeviceInfo} />
      <Button title="Get WiFi Info" onPress={getWifiInfo} disabled={isLoadingWifiInfo} />
    </View>
  );
};

export default HomeScreen;