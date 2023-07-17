import React, { useState, useCallback, useEffect } from 'react';
import { Button, View, Text, Modal } from 'react-native';
import { getSyncDeviceInfo, getAsyncDeviceInfo } from '../services/GetDeviceInfo';
import { PermissionsAndroid } from 'react-native';
import WifiManager from 'react-native-wifi-reborn';
import NetInfo from "@react-native-community/netinfo";

const HomeScreen = ({ navigation }) => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [requestedInfo, setRequestedInfo] = useState('');
  const [locationGranted, setLocationGranted] = useState('');
  const [isLoadingDeviceInfo, setIsLoadingDeviceInfo] = useState(false);
  const [isLoadingApInfo, setIsLoadingApInfo] = useState(false);
  const [isLoadingDeviceNetworkInfo, setIsLoadingDeviceNetworkInfo] = useState(false);

  useEffect(() => {
    /**
     * required for reading list of APs
     */
    PermissionsAndroid.requestMultiple([
      PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
    ]).then(result => {
      if (result['android.permission.ACCESS_FINE_LOCATION'] === 'granted') {
        setLocationGranted('ALLOW');
      }
    })
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
    </View>
  );
};

export default HomeScreen;