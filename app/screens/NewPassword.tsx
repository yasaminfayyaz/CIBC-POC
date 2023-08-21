import * as React from 'react';
import { useState, useCallback } from 'react';
import { Button, Text, TextInput, View, Alert, useWindowDimensions, StyleSheet } from 'react-native';
import { applicationStore } from '../store/applicationStore';
import { setPassword } from '../services/User';
import { Loader } from '../components/Loader/Loader';

const LandingScreen = ({ route, navigation }) => {
    const { username } = route.params;
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [isUpdatingPassword, setIsUpdatingPassword] = useState(false);
    const { width, height } = useWindowDimensions();

    const navigateToSignInScreen = () => navigation.pop();

    const doPasswordUpdate = useCallback(async () => {
        if (username && oldPassword && newPassword) {
            setIsUpdatingPassword(true);
            const response = await setPassword(username, oldPassword, newPassword);
            setIsUpdatingPassword(false);

            if (response.code === 1001 || response.code === 1002) {
                Alert.alert('Password update error', 'Incorrect password', [{ text: 'Ok', style: 'default' }]);
            } else if (response.code === 0) {
                Alert.alert('Success', 'Password updated!', [{ text: 'Ok', style: 'default', onPress: navigateToSignInScreen }]);
            }

        } else {
            Alert.alert('Sign in error', 'Please enter username and password', [{ text: 'Ok', style: 'default' }]);
        }
    }, [oldPassword, newPassword])

    return (
        <>
            <Loader visible={isUpdatingPassword} />
            <View style={styleFactory(isUpdatingPassword).mainView}>
                <Text>Set New Password</Text>
                <TextInput
                    onChangeText={setOldPassword}
                    value={oldPassword}
                    placeholder='Type old password'
                    autoCapitalize='none'
                    autoComplete='off'
                    autoCorrect={false}
                    secureTextEntry={true}
                    style={styleFactory(undefined, width, height).textInputStyle}
                />
                <TextInput
                    onChangeText={setNewPassword}
                    value={newPassword}
                    placeholder='Type new password'
                    autoCapitalize='none'
                    autoComplete='off'
                    autoCorrect={false}
                    secureTextEntry={true}
                    style={styleFactory(undefined, width, height).textInputStyle}
                />
                <Button
                    title="Submit"
                    onPress={doPasswordUpdate}
                    disabled={isUpdatingPassword}
                />
            </View>
        </>
    );
};

const styleFactory = (isUpdatingPassword?: boolean, width?: number, height?: number) => StyleSheet.create({
    mainView: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        opacity: isUpdatingPassword ? 0.25 : 1.00
    },
    textInputStyle: {
        borderColor: 'black',
        borderWidth: 0.5,
        width: width * 40 / 100,
        textAlign: 'center',
        height: height * 5 / 100,
        marginVertical: 5
    }
})

export default LandingScreen;