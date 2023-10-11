/**
 * This screen is the main screen of the project.
 * This component is used to collect contextual information, including device info, network info, etc.
 *
 * Additionally, this component also queries the API for the acceptable access points, which are used
 * to determine indoor location.
 *
 * Finally, this component also queries the API for the available resources one will have access to,
 * based on the collected contextual information.
 */
import React, {useState, useCallback, useEffect} from 'react';
import {
  Button,
  View,
  Text,
  SafeAreaView,
  FlatList,
  StyleSheet,
  Pressable,
  Alert,
} from 'react-native';
import {InstalledApps} from 'react-native-launcher-kit';
import Geolocation from '@react-native-community/geolocation';
import {getResources} from '../services/Resources';
import {
  getBrand,
  getFirstInstallTime,
  getUniqueId,
  isEmulator,
  isPinOrFingerprintSet,
} from 'react-native-device-info';

import {applicationStore} from '../store/applicationStore';
import {Resource} from '../types/Resource';
import {
  AccessRequest,
  CurrentLocation,
  CurrentLocationCoords,
  DeviceInfo,
  InstalledApp,
} from '../types/AccessRequestTypes';
import {postAccessRequest} from '../services/AccessRequest';

const HomeScreen = ({navigation}) => {
  const bssids = applicationStore.useState(s => s.desiredBSSIDs);
  const token = applicationStore.useState(s => s.userToken);

  const [resources, setResources] = useState<Resource[]>([]);
  const [installedApps, setInstalledApps] = useState<InstalledApp[]>();
  const [currentLocationCoords, setCurrentLocationCoords] = useState<CurrentLocationCoords>();
  const [currentLocation, setCurrentLocation] = useState<CurrentLocation>();
  const [deviceInfo, setDeviceInfo] = useState<DeviceInfo>();
  const [isGettingResources, setIsGettingResources] = useState(false);
  const [isSendingAccessRequest, setIsSendingAccessRequest] = useState(false);

  const getInstalledApps = useCallback(() => {
    if (installedApps === undefined) {
      const allInstalledApps = InstalledApps.getSortedApps();
      const apps = allInstalledApps.map(ia => ({packageName: ia.packageName}));
      setInstalledApps(apps);
    }
  }, [installedApps]);

  const getCurrentLocation = useCallback(() => {
    if (currentLocationCoords === undefined || currentLocation === undefined) {
      Geolocation.getCurrentPosition(locationInfo => {
        const lat = locationInfo.coords.latitude;
        const lon = locationInfo.coords.longitude;
        const mocked = locationInfo.mocked;
        setCurrentLocationCoords({latitude: lat, longitude: lon});
        setCurrentLocation(mocked);
      });
    }
  }, [currentLocationCoords]);

  const getDeviceInfo = useCallback(async () => {
    if (deviceInfo === undefined) {
      const uniqueId = await getUniqueId();
      const pinOrFingerprintSet = await isPinOrFingerprintSet();
      const emulator = await isEmulator();
      const brand = getBrand();
      const firstInstallTime = await getFirstInstallTime();
      setDeviceInfo({uniqueId, pinOrFingerprintSet, emulator, brand, firstInstallTime});
    }
  }, [deviceInfo]);

  const getAvailableResources = useCallback(async () => {
    setIsGettingResources(true);
    const availableResources = await getResources(token);
    setIsGettingResources(false);
    setResources(availableResources.resources);
  }, [resources]);

  const sendAccessRequest = useCallback(
    async (resourceId: number, actionID: string) => {
      setIsSendingAccessRequest(true);
      if (installedApps && currentLocationCoords && currentLocation !== undefined && deviceInfo) {
        const contextualInfo: AccessRequest = {
          ResourceID: resourceId,
          ActionID: actionID,
          installedApps,
          CurrentLocationCoords: currentLocationCoords,
          DeviceInfo: deviceInfo,
          CurrentLocation: currentLocation,
        };
        const accessRequestResult = await postAccessRequest(contextualInfo, token);
        Alert.alert(`Code: ${accessRequestResult.code}`, accessRequestResult.message, [
          {text: 'Ok'},
        ]);
      }
      setIsSendingAccessRequest(false);
    },
    [installedApps, currentLocationCoords, currentLocation, deviceInfo],
  );

  useEffect(() => {
    getInstalledApps();
    getCurrentLocation();
    getDeviceInfo();
  }, []);

  useEffect(() => {
    if (resources && resources.length === 0) getAvailableResources();
  }, [resources]);

  const handleItemPress = (resource: Resource) => {
    Alert.alert('Choose action', 'What type of access request are you performing? ', [
      {
        text: 'Read',
        onPress: () => sendAccessRequest(resource.resourceID, 'read'),
      },
      {
        text: 'Write',
        onPress: () => sendAccessRequest(resource.resourceID, 'write'),
      },
    ]);
  };

  const handleLogout = () => {
    applicationStore.update(applicationState => {
      applicationState.userToken = undefined;
    });
  };

  return (
    <SafeAreaView style={styles.safeAreaViewContainer}>
      {isGettingResources ? (
        <>
          <View>
            <Text>Loading Resources</Text>
          </View>
        </>
      ) : (
        <>
          <View style={styles.documentListContainer}>
            <FlatList
              data={resources}
              renderItem={({item}) => (
                <Pressable
                  style={({pressed}) =>
                    pressed ? styles.documentItemContainerPressed : styles.documentItemContainer
                  }
                  onPress={() => handleItemPress(item)}>
                  <Text style={{fontSize: 20}}>{item.resourceName}</Text>
                  <Text>{item.resourceID}</Text>
                </Pressable>
              )}
            />
          </View>
          <View style={styles.logoutView}>
            <Button
              title="Logout"
              onPress={() =>
                Alert.alert('Logout', 'Confirm logout?', [
                  {text: 'No', style: 'default'},
                  {text: 'Yes', style: 'destructive', onPress: handleLogout},
                ])
              }
            />
          </View>
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
    flexDirection: 'column',
  },
  documentItemContainer: {
    flex: 1,
    backgroundColor: '#dedede',
    padding: 10,
    margin: 5,
  },
  documentItemContainerPressed: {
    flex: 1,
    backgroundColor: '#dedede',
    padding: 10,
    margin: 5,
    opacity: 0.5,
  },
  logoutView: {
    flex: 0,
  },
});

export default HomeScreen;
