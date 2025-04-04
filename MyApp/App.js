import React, { useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';

// ---------- 로그인 화면 ----------
function LoginScreen({ navigation }) {
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    if (!userId || !password) {
      Alert.alert('오류', '아이디와 비밀번호를 모두 입력해주세요.');
      return;
    }

    if (userId === 'dgu123' && password === '1234') {
      navigation.replace('MainTab', { userId });
    } else {
      Alert.alert('로그인 실패', '아이디 또는 비밀번호가 올바르지 않습니다.');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>로그인</Text>
      <TextInput
        style={styles.input}
        placeholder="아이디 입력"
        value={userId}
        onChangeText={setUserId}
      />
      <TextInput
        style={styles.input}
        placeholder="비밀번호 입력"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button title="로그인" onPress={handleLogin} />
      <View style={{ marginTop: 10 }}>
        <Button title="회원가입" onPress={() => navigation.navigate('Signup')} />
      </View>
    </View>
  );
}

// ---------- 회원가입 화면 ----------
function SignupScreen({ navigation }) {
  const [newId, setNewId] = useState('');
  const [newPassword, setNewPassword] = useState('');

  const handleSignup = () => {
    if (!newId || !newPassword) {
      Alert.alert('오류', '아이디와 비밀번호를 모두 입력해주세요.');
      return;
    }

    // 실제 앱에서는 백엔드에 저장하는 로직 필요
    Alert.alert('회원가입 성공', `${newId}님, 환영합니다!`);
    navigation.replace('Login');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>회원가입</Text>
      <TextInput
        style={styles.input}
        placeholder="새 아이디 입력"
        value={newId}
        onChangeText={setNewId}
      />
      <TextInput
        style={styles.input}
        placeholder="새 비밀번호 입력"
        value={newPassword}
        onChangeText={setNewPassword}
        secureTextEntry
      />
      <Button title="회원가입 완료" onPress={handleSignup} />
    </View>
  );
}

// ---------- 홈 화면 ----------
function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>홈 화면</Text>
    </View>
  );
}

// ---------- 프로필 화면 (로그아웃 포함) ----------
function ProfileScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>내 정보</Text>
      <Button title="로그아웃" onPress={() => navigation.replace('Login')} />
    </View>
  );
}

// ---------- 하단 탭 네비게이션 ----------
const Tab = createBottomTabNavigator();

function MainTab() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeScreen} options={{ title: '홈' }} />
      <Tab.Screen name="Profile" component={ProfileScreen} options={{ title: '내 정보' }} />
    </Tab.Navigator>
  );
}

// ---------- Stack 네비게이션 ----------
const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login" screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Signup" component={SignupScreen} />
        <Stack.Screen name="MainTab" component={MainTab} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// ---------- 스타일 ----------
const styles = StyleSheet.create({
  container: {
    flex: 1, justifyContent: 'center', paddingHorizontal: 20, backgroundColor: '#fff'
  },
  title: {
    fontSize: 28, fontWeight: 'bold', textAlign: 'center', marginBottom: 30
  },
  input: {
    height: 50, borderColor: '#ccc', borderWidth: 1, borderRadius: 8,
    paddingHorizontal: 10, marginBottom: 15
  }
});
 