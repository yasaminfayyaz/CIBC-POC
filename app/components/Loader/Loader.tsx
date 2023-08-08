import { View, ActivityIndicator, Modal, StyleSheet, useWindowDimensions, Text } from 'react-native';

type LoaderProps = {
    visible: boolean;
}

export const Loader = (props: LoaderProps) => {
    const { width, height } = useWindowDimensions();
    const ratio = width / height;
    const styles = getStyles((width * 20 / 100), ((height * ratio) * 20 / 100), (height - ((height * ratio) * 20 / 100)) / 2)

    return (
        <Modal visible={props.visible} transparent={true}>
            <View style={styles.modalContainer}>
                <ActivityIndicator />
                <Text>Loading...</Text>
            </View>
        </Modal>
    );
}

const getStyles = (width: number, height: number, marginVertical: number) => StyleSheet.create({
    modalContainer: {
        width: width,
        height: height,
        alignContent: 'center',
        alignItems: 'center',
        alignSelf: 'center',
        verticalAlign: 'middle',
        justifyContent: 'center',
        backgroundColor: 'white',
        borderRadius: 10,
        marginVertical: marginVertical
    }
});