import React from 'react';
import { useState, useEffect } from 'react';
import { View, Text } from 'react-native';
import { getManufacturer } from 'react-native-device-info';

export const DeviceManufacturer = () => {
    const [manufacturer, setManufacturer] = useState('');

    useEffect(() => {
        if (!manufacturer) {
            getManufacturer().then(deviceManufacturer => {
                setManufacturer(deviceManufacturer);
            }).catch(err => {
                setManufacturer('Error getting manufacturer');
            });
        }
    }, [manufacturer]);

    return (
        <View>
            <Text>{manufacturer}</Text>
        </View>
    );
};