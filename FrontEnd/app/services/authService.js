import api from '../config/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const authService = {
  // 회원가입
  async signup(email, password, nickname) {
    try {
      console.log('회원가입 요청 데이터:', { email, password, nickname });
      const response = await api.post('/signup', {
        email,
        password,
        nickname,
      });
      console.log('회원가입 응답:', response.data);
      return response.data;
    } catch (error) {
      console.error('회원가입 서비스 에러:', error);
      throw error;
    }
  },

  // 로그인
  async login(email, password) {
    try {
      const response = await api.post('/login', {
        email,
        password,
      });
      const { access_token } = response.data;
      await AsyncStorage.setItem('access_token', access_token);
      return response.data;
    } catch (error) {
      console.error('로그인 서비스 에러:', error);
      throw error;
    }
  },

  // 로그아웃
  async logout() {
    try {
      await AsyncStorage.removeItem('access_token');
    } catch (error) {
      console.error('로그아웃 서비스 에러:', error);
      throw error;
    }
  },

  // 프로필 조회
  async getProfile() {
    try {
      const response = await api.get('/user/profile');
      return response.data;
    } catch (error) {
      console.error('프로필 조회 서비스 에러:', error);
      throw error;
    }
  },

  // 토큰 존재 여부 확인
  async isAuthenticated() {
    try {
      const token = await AsyncStorage.getItem('access_token');
      return !!token;
    } catch (error) {
      console.error('인증 확인 서비스 에러:', error);
      return false;
    }
  },
}; 