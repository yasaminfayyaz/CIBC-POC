import * as React from 'react';
import { useState, useCallback, useEffect, useRef } from 'react';
import { Button, Text, TextInput, View, Alert, useWindowDimensions } from 'react-native';
import { getBssids } from '../services/GetBssids';
import { applicationStore } from '../store/applicationStore';
import { BSSID } from '../types/BSSID';
import { login } from '../services/User';
import { Loader } from '../components/Loader/Loader';

const LandingScreen = ({ navigation }) => {
  const token = applicationStore.useState(s => s.userToken);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isDoingSignIn, setIsDoingSignIn] = useState(false);
  const [desiredBssids, setDesiredBssids] = useState<Array<BSSID>>();
  const passswdRef = useRef();

  const { width, height } = useWindowDimensions();

  useEffect(() => {
    if (token) {
      applicationStore.update(applicationState => {
        applicationState.userToken = undefined;
      });
    }
    if (!desiredBssids) {
      getBssids().then(resp => {
        setDesiredBssids(resp);
      });
    }
  }, []);

  useEffect(() => {
    if (desiredBssids) {
      applicationStore.update(applicationState => {
        applicationState.desiredBSSIDs = desiredBssids;
      });
    }
  }, [desiredBssids]);

  const navigateToUpdatePassword = () => navigation.push("NewPasswordScreen", { username });

  const doSignIn = useCallback(async () => {
    if (username && password) {
      setIsDoingSignIn(true);
      const response = await login(username, password);
      setIsDoingSignIn(false);

      if (response.code === 1001 || response.code === 1002) {
        Alert.alert('Sign in error', 'Incorrect username or password', [{ text: 'Ok', style: 'default' }]);
      } else if (response.code === 1000) {
        applicationStore.update(applicationState => {
          applicationState.userToken = response.token;
        });
        Alert.alert('First login detected', 'Please set a new password', [{ text: 'Ok', style: 'default', onPress: navigateToUpdatePassword }])
      } else if (response.code === 0) {
        applicationStore.update(applicationState => {
          applicationState.userToken = response.token;
        });
      }

    } else {
      Alert.alert('Sign in error', 'Please enter username and password', [{ text: 'Ok', style: 'default' }]);
    }
  }, [username, password])

  return (
    <>
      <Loader visible={isDoingSignIn} />
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', opacity: isDoingSignIn ? 0.25 : 1.00 }}>
        <Text>CIBC POC</Text>
        <TextInput
          onChangeText={setUsername}
          value={username}
          placeholder="Type username"
          autoCapitalize='none'
          autoComplete='off'
          autoCorrect={false}
          style={{ borderColor: 'black', borderWidth: 0.5, width: width * 40 / 100, textAlign: 'center', height: height * 5 / 100, marginVertical: 5 }}
          returnKeyType='next'
          onSubmitEditing={() => { passswdRef.current.focus() }}
          blurOnSubmit={false}
        />
        <TextInput
          onChangeText={setPassword}
          value={password}
          placeholder='Type password'
          autoCapitalize='none'
          autoComplete='off'
          autoCorrect={false}
          secureTextEntry={true}
          style={{ borderColor: 'black', borderWidth: 0.5, width: width * 40 / 100, textAlign: 'center', height: height * 5 / 100, marginVertical: 5 }}
          ref={passswdRef}
        />
        <Button
          title="Submit"
          onPress={doSignIn}
          disabled={isDoingSignIn}
        />
      </View>
    </>
  );
};

export default LandingScreen;