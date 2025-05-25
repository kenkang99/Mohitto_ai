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
      
      if (!response.data.access_token) {
        throw new Error('토큰이 없습니다.');
      }

      // 토큰 저장
      await AsyncStorage.setItem('userToken', response.data.access_token);
      await AsyncStorage.setItem('access_token', response.data.access_token);
      
      return {
        token: response.data.access_token,
        user: response.data.user
      };
    } catch (error) {
      console.error('로그인 서비스 에러:', error);
      throw error;
    }
  },

  // 로그아웃
  async logout() {
    try {
      await AsyncStorage.removeItem('userToken');
    } catch (error) {
      console.error('로그아웃 서비스 에러:', error);
      throw error;
    }
  },

  // 프로필 조회
  async getProfile() {
    try {
      const token = await AsyncStorage.getItem('userToken');
      if (!token) {
        throw new Error('인증되지 않은 사용자입니다.');
      }

      const response = await api.get('/user/profile', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('프로필 조회 서비스 에러:', error);
      throw error;
    }
  },

  // 토큰 존재 여부 확인
  async isAuthenticated() {
    try {
      const token = await AsyncStorage.getItem('userToken');
      return !!token;
    } catch (error) {
      console.error('인증 확인 서비스 에러:', error);
      return false;
    }
  },
}; 