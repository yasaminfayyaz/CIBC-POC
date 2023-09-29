import {useState, useEffect} from 'react';

import {
    Accelerometer,
    Barometer,
    DeviceMotion,
    Gyroscope,
    LightSensor,
    Magnetometer,
    MagnetometerUncalibrated,
    Pedometer,
  } from 'expo-sensors';

const [{ x, y, z }, setAccelData] = useState({ x: 0, y: 0, z: 0 });
const [accelSubscription, setAccelSubscription] = useState(null);
const _accelSlow = () => Accelerometer.setUpdateInterval(1000);
const _accelFast = () => Accelerometer.setUpdateInterval(16);
const _accelSubscribe = () => {
setAccelSubscription(Accelerometer.addListener(setAccelData));
}
const _accelUnsubscribe = () => {
accelSubscription && accelSubscription.remove();
setAccelSubscription(null);
}
useEffect(() => {
_accelSubscribe();
return () => _accelUnsubscribe();
}, []);