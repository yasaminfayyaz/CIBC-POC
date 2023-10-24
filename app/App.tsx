import React from 'react';
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { applicationStore } from './store/applicationStore';

import LandingScreen from './screens/LandingScreen';
import NewPasswordScreen from './screens/NewPassword';
import HomeScreen from './screens/HomeScreen';
import DetailsScreen from './screens/DetailsScreen';

const Stack = createNativeStackNavigator();

function App(): JSX.Element {
  /**
   * everytime the app opens, we prompt to sign in, so we dont need to look for token in application securestorage
   * after sign in, save token or what ever result in application context
   */
  const userToken = applicationStore.useState(s => s.userToken);

  return (
    <NavigationContainer>
      <Stack.Navigator>
        {userToken === undefined ? (
          <>
            <Stack.Screen name="Sign In Screen" component={LandingScreen} options={{ headerShown: false }} />
            <Stack.Screen name="NewPasswordScreen" component={NewPasswordScreen} options={{ headerShown: false }} />
          </>
        ) : (
          <>
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="Details" component={DetailsScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );

  // return (
  //   <NavigationContainer>
  //     <Stack.Navigator initialRouteName='Landing'>
  //       <Stack.Screen name="Landing" component={LandingScreen} options={{ title: 'Landing' }} />
  //       <Stack.Screen name="Home" component={HomeScreen} options={{ title: 'Overview' }} />
  //       <Stack.Screen name="Details" component={DetailsScreen} />
  //     </Stack.Navigator>
  //   </NavigationContainer>
  // );
}

export default App;
