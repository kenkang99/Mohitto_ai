import React from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';

export default function HomeScreen() {
  const router = useRouter();

  return (
    <View style={{ flex: 1 }}>
      {/* 위쪽 절반 */}
      <View style={{ flex: 1.3, backgroundColor: '#FFBCC2', justifyContent: 'center', alignItems: 'center' }}>
        <Image source={require('../../assets/logo.png')} style={styles.image} />
      </View>

      {/* 아래쪽 절반 */}
      <View style={{
        flex: 1,
        backgroundColor: 'white',
        justifyContent: 'flex-start',
        alignItems: 'center',
        gap: 20
      }}>
        <Text style={{ fontSize: 30, marginTop: 50, fontWeight: 'bold', color: '#3F414E' }}>
          We are What we do
        </Text>
        <Text style={{ color: "#A1A4B2" }}>
          Crafting Your Perfect Hair Style with AI
        </Text>

        <TouchableOpacity style={styles.button} onPress={() => router.push('/signup')}>
          <Text style={styles.buttonText}>SIGN UP</Text>
        </TouchableOpacity>

        <View style={{ flexDirection: 'row' }}>
          <Text style={{ color: '#A1A4B2' }}>ALREADY HAVE AN ACCOUNT?</Text>
          <TouchableOpacity onPress={() => router.push('/signin')}>
            <Text style={{ color: '#FFBCC2' }}>  LOG IN</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  button: {
    width:'90%',
    backgroundColor: '#FFBCC2',
    paddingVertical: 17,
    paddingHorizontal: 150,
    borderRadius: 10,
  },
  buttonText: {
    color: '#F6F1FB',
    fontSize: 15,
    fontWeight: 'bold',
  },
  loginLink: {
    color: '#FFBCC2',
    fontWeight: 'bold',
  },
  image: {
    width: 200,
    height: 200,
    resizeMode: 'contain',
  },
});
