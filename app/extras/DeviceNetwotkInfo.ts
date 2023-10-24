import {useState, useEffect, useCallback} from 'react';
import NetInfo, { NetInfoState } from "@react-native-community/netinfo";

const [deviceNetworkInfo, setDeviceNetworkInfo] = useState<NetInfoState>();

const getDeviceNetworkInfo = useCallback(() => {
    NetInfo.fetch().then(result => {
        setDeviceNetworkInfo(result);
    }).finally(() => {
    });
}, [deviceNetworkInfo]);

useEffect(() => {
    if (!deviceNetworkInfo) getDeviceNetworkInfo();
}, [deviceNetworkInfo]);