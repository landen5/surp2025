import React, { useState } from "react";
import {
  Text, View, TextInput, TouchableOpacity, StyleSheet, Alert,
  Platform, ScrollView
} from "react-native";
import * as Location from 'expo-location';

export default function Index() {
  const [userData, setUserData] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [responseData, setResponseData] = useState(null);
  const [coarseLocation, setCoarseLocation] = useState<{ latitude: number; longitude: number; accuracy: number } | null>(null);
  const [isFetchingLocation, setIsFetchingLocation] = useState(false);
  const API_URL = Platform.OS === 'android'
    ? 'http://10.0.2.2:5050/api/data'
    : 'http://127.0.0.1:5050/api/data';

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

  const getCoarseLocation = async () => {
    if (isFetchingLocation) return;
    setIsFetchingLocation(true);
    try {
      // request and fetch via expo-location
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== Location.PermissionStatus.GRANTED) {
        Alert.alert('Permission denied', 'Cannot fetch location.');
        return;
      }
      const loc = await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Lowest });
      const latitude = loc.coords.latitude ?? 0;
      const longitude = loc.coords.longitude ?? 0;
      const accuracy = loc.coords.accuracy ?? 0;
      setCoarseLocation({ latitude, longitude, accuracy });
      Alert.alert('Location fetched', 'Got approximate location');
    } catch (e) {
      console.error(e);
      Alert.alert('Error', 'Unexpected error fetching location.');
    } finally {
      setIsFetchingLocation(false);
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
        
        <TouchableOpacity
          style={styles.button}
          onPress={getCoarseLocation}
          disabled={isFetchingLocation}
        >
          <Text style={styles.buttonText}>
            {isFetchingLocation ? 'Fetching Location...' : 'Get Coarse Location'}
          </Text>
        </TouchableOpacity>

        {responseData && (
          <View style={styles.responseContainer}>
            <Text style={styles.responseTitle}>Server Response:</Text>
            <Text style={styles.responseText}>
              {JSON.stringify(responseData, null, 2)}
            </Text>
          </View>
        )}
        {coarseLocation && (
          <View style={styles.responseContainer}>
            <Text style={styles.responseTitle}>Coarse Location:</Text>
            <Text style={styles.responseText}>
              {JSON.stringify(coarseLocation, null, 2)}
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