import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, TouchableOpacity, Image } from 'react-native';
import { useRouter } from 'expo-router';
import Checkbox from 'expo-checkbox';
import { Ionicons } from '@expo/vector-icons';

function TermsCheck({ isChecked, setChecked }) {
  return (
    <View style={styles.checkboxRow}>
      <Text style={styles.policyText}>
        i have read the <Text style={styles.linkText}> Privace Policy</Text>
      </Text>
      <Checkbox
        value={isChecked}
        onValueChange={setChecked}
        color={isChecked ? '#FFBCC2' : '#A1A4B2'}
      />
    </View>
  );
}

export default function SignUpScreen() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isChecked, setChecked] = useState(false);

  const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSignUp = () => {
    if (!email.trim()) {
      alert('이메일을 입력해 주세요.');
      return;
    }
    if (!isValidEmail(email)) {
      alert('이메일 형식이 올바르지 않습니다.');
      return;
    }
    console.log('회원가입 정보:', { name, email, password });
    alert('회원가입 완료!');
    router.back();
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
        <Text style={styles.backButtonText}>←</Text>
      </TouchableOpacity>

      <Text style={styles.title}>Create your account</Text>

      <TouchableOpacity style={styles.fbButton} onPress={() => console.log('Facebook')}>
        <View style={styles.fbButtonContent}>
          <Image source={require('../../assets/fblogo.png')} style={styles.fbicon} />
          <Text style={styles.fbButtonText}>CONTINUE WITH FACEBOOK</Text>
        </View>
      </TouchableOpacity>

      <TouchableOpacity style={styles.GgButton} onPress={() => console.log('Google')}>
        <View style={styles.GgButtonContent}>
          <Image source={require('../../assets/Gglogo.png')} style={styles.Ggicon} />
          <Text style={styles.GgButtonText}>CONTINUE WITH GOOGLE</Text>
        </View>
      </TouchableOpacity>

      <Text style={{ color: '#A1A4B2', fontWeight: '600',fontSize: 13 }}>
        OR LOGIN WITH EMAIL
      </Text>

      <View>
        <TextInput
          placeholder="Name"
          style={styles.inputbase}
          value={name}
          onChangeText={setName}
        />
        <View style={styles.inputWithIcon}>
          <TextInput
            placeholder="Email"
            style={styles.inputField}
            keyboardType="email-address"
            autoCapitalize="none"
            value={email}
            onChangeText={setEmail}
          />
          {isValidEmail(email) && (
            <Ionicons name="checkmark-circle" size={15} color="green" />
          )}
        </View>
        <TextInput
          placeholder="Password"
          style={styles.inputbase}
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />
      </View>

      <TermsCheck isChecked={isChecked} setChecked={setChecked} />

      <TouchableOpacity onPress={handleSignUp} style={styles.submitButton}>
        <View style={styles.submitButtonContent}>
          <Text style={styles.submitButtonText}>GET STARTED</Text>
        </View>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 100,
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  
  title: {
    fontWeight: 'bold',
    fontSize: 25,
    textAlign: 'center',
    marginBottom: 30,
    color: '#3F414E',
    bottom : 20
  },
  backButton: {
    position: 'absolute',
    top: 20,
    left: 20,
    width: 50,  
    height: 50,
    backgroundColor: 'white',
    paddingHorizontal: 10,
    paddingVertical: 10,
    borderRadius: 50,
    borderColor: 'lightgray',
    borderWidth: 1,
    alignItems: 'center',
    zIndex: 1,
  },
  backButtonText: {
    fontSize: 20,
    color: 'black',
    fontWeight: 'bold',
  },
  inputbase: {
    width: 360,
    height: 50,
    backgroundColor: '#F2F3F7',
    borderRadius: 10,
    padding: 12,
    marginBottom: 20,
    fontSize: 16,
    marginTop: 20,
  },
  fbButton: {
    backgroundColor: '#FFBCC2',
    paddingVertical: 17,
    paddingHorizontal: 75,
    borderRadius: 10,
    marginBottom: 20,
    bottom : 20
  },
  fbButtonText: {
    color: '#F6F1FB',
    fontWeight: '500',
  },
  fbButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  fbicon: {
    width: 10,
    height: 20,
    marginRight: 10,
  },
  GgButton: {
    paddingVertical: 17,
    paddingHorizontal: 73,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#F2F2F2',
    bottom : 20,
  },
  GgButtonText: {
    color: '#3F414E',
    fontWeight: '500',
  },
  GgButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  Ggicon: {
    width: 20,
    height: 22,
    marginRight: 20,
  },
  checkboxRow: {
    width: 410,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 28,
    justifyContent: 'space-between',
  },
  policyText: {
    color: '#A1A4B2',
    marginLeft: 0,
    textAlign: 'left',
    alignItems: 'flex-start',
  },
  linkText: {
    color: '#FFBCC2',
  },
  submitButton: {
    backgroundColor: '#FFBCC2',
    paddingVertical: 17,
    paddingHorizontal: 130,
    borderRadius: 10,
    marginTop: 30,
  },
  submitButtonText: {
    color: '#F2F2F2',
  },
  submitButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  inputWithIcon: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F2F2F2',
    paddingHorizontal: 12,
    width: 360,
    height: 50,
    borderRadius: 10,
  },
  inputField: {
    flex: 1,
    fontSize: 16,
  },
});
