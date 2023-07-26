import * as React from 'react';
import { useState, useCallback } from 'react';
import { Button, Text, TextInput, View } from 'react-native';
import { applicationStore } from '../store/applicationStore';

const LandingScreen = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [passwd, setPasswd] = useState('');

  const doSignIn = useCallback(() => {
    /**
     * if sign in is successful, update application store's userToken
     */

    if (username && passwd) {
      applicationStore.update(applicationState => {
        applicationState.userToken = "myApplicationToken";
      });
    } else {
      console.error("Type your username and password");
    }
  }, [username, passwd])

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>CIBC POC</Text>
      <TextInput
        onChangeText={setUsername}
        value={username}
        placeholder="Type username"
        autoCapitalize='none'
        autoComplete='off'
        autoCorrect={false}
      />
      <TextInput
        onChangeText={setPasswd}
        value={passwd}
        placeholder='Type password'
        autoCapitalize='none'
        autoComplete='off'
        autoCorrect={false}
        secureTextEntry={true}
      />
      <Button
        title="Submit"
        onPress={doSignIn}
      />
    </View>
  );
};

export default LandingScreen;