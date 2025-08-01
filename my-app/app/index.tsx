import React, { useState } from "react";
import { 
  Text, 
  View, 
  TextInput, 
  TouchableOpacity, 
  StyleSheet, 
  Alert, 
  Platform,
  ScrollView 
} from "react-native";
import * as Location from 'expo-location';

export default function Index() {
  const [userData, setUserData] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [responseData, setResponseData] = useState(null);
  const [location, setLocation] = useState<Location.LocationObjectCoords | null>(null);
  const [isFetchingLocation, setIsFetchingLocation] = useState(false);
  const API_URL = 'https://surp2025.duckdns.org/api/data'; 

  // fetch approximate device location
  const getCoarseLocation = async () => {
    if (isFetchingLocation) return;
    setIsFetchingLocation(true);
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== Location.PermissionStatus.GRANTED) {
        Alert.alert('Permission denied', 'Cannot fetch location.');
        return;
      }
      const loc = await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Lowest });
      setLocation(loc.coords);
    } catch (e) {
      console.error(e);
      Alert.alert('Error', 'Unable to get location.');
    } finally {
      setIsFetchingLocation(false);
    }
  };

  const sendData = async () => {
    if (!userData.trim()) {
      Alert.alert('Error', 'Please enter some data to send');
      return;
    }

    setIsSending(true);
    
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userInput: userData,
          timestamp: new Date().toISOString(),
          deviceInfo: {
            platform: Platform.OS,
            version: Platform.Version,
          },
          location: location ? {
            latitude: location.latitude,
            longitude: location.longitude,
            accuracy: location.accuracy,
          } : null,
        }),
      });

      const result = await response.json();
      setResponseData(result);
      
      Alert.alert('Success', 'Data sent successfully');
      console.log('Server response:', result);
    } catch (error) {
      console.error('Error sending data:', error);
      Alert.alert('Error', 'Failed to send data. Check your connection and server status.');
    } finally {
      setIsSending(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.scrollContainer}>
      <View style={styles.container}>
        <Text style={styles.title}>Data Minimization Research</Text>
        
        <View style={styles.infoBox}>
          <Text style={styles.infoText}>
            This app sends unencrypted data to a Flask backend for privacy research purposes.
            The network traffic can be examined.
          </Text>
        </View>
        
        <Text style={styles.inputLabel}>Enter data to send (will be sent unencrypted):</Text>
        <TextInput
          style={styles.input}
          value={userData}
          onChangeText={setUserData}
          placeholder="Enter personal data (name, email, etc.)"
          multiline
        />
        
        <TouchableOpacity 
          style={styles.button} 
          onPress={sendData}
          disabled={isSending}
        >
          <Text style={styles.buttonText}>
            {isSending ? 'Sending...' : 'Send Data'}
          </Text>
        </TouchableOpacity>
        
        {/* location button */}
        <TouchableOpacity
          style={[styles.button, { marginTop: 12 }]}
          onPress={getCoarseLocation}
          disabled={isFetchingLocation}
        >
          <Text style={styles.buttonText}>
            {isFetchingLocation ? 'Fetching...' : 'Get Location'}
          </Text>
        </TouchableOpacity>

        {/* display location info */}
        {location && (
          <View style={styles.responseContainer}>
            <Text style={styles.responseTitle}>Location Info:</Text>
            <Text style={styles.responseText}>
              {`Latitude: ${location.latitude}\nLongitude: ${location.longitude}\nAccuracy: ${location.accuracy}m`}
            </Text>
          </View>
        )}

        {responseData && (
          <View style={styles.responseContainer}>
            <Text style={styles.responseTitle}>Server Response:</Text>
            <Text style={styles.responseText}>
              {JSON.stringify(responseData, null, 2)}
            </Text>
          </View>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scrollContainer: {
    flexGrow: 1,
  },
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  infoBox: {
    backgroundColor: '#e6f7ff',
    borderRadius: 8,
    padding: 15,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#91d5ff',
  },
  infoText: {
    fontSize: 14,
    color: '#0050b3',
  },
  inputLabel: {
    fontSize: 16,
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
    minHeight: 100,
    backgroundColor: '#fff',
    marginBottom: 20,
    textAlignVertical: 'top',
  },
  button: {
    backgroundColor: '#1677ff',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  responseContainer: {
    marginTop: 20,
    padding: 15,
    backgroundColor: '#f6ffed',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#b7eb8f',
  },
  responseTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  responseText: {
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    fontSize: 12,
  }
});