import React from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet,ScrollView,Linking } from 'react-native';
import { useRouter, usePathname} from 'expo-router';

export default function MypageHairshop() {
  const router = useRouter();
  const pathname = usePathname();

  const shops = [{
    id : 1,
    name :'하츠도산',
    desc : '세련된 분위기의 최신 트렌드를 반영한 서비스',
    style : '리프컷 , 드롭컷 ,가일컷',
    location:'서울시 강남구 압구정동 189로',
    tel : '02 - 1010 -1010',
    link : 'https://map.naver.com/p/entry/place/1710391167?lng=127.0350643&lat=37.5234158&placePath=%2Fhome&entry=plt&searchType=place&c=15.00,0,0,0,dh'
  },
  {
    id : 2,
    name :'하츠도산',
    desc : '세련된 분위기의 최신 트렌드를 반영한 서비스',
    style : '리프컷 , 드롭컷 ,가일컷',
    location:'서울시 강남구 압구정동 189로',
    tel : '02 - 1010 -1010',
    link : 'https://map.naver.com/p/entry/place/1710391167?lng=127.0350643&lat=37.5234158&placePath=%2Fhome&entry=plt&searchType=place&c=15.00,0,0,0,dh'
  

  }]

  return (
    <View style={{ flex: 1 ,backgroundColor: 'white'}}>
        <View style={styles.header}>
          <TouchableOpacity onPress={()=>router.push('/welcome')}>
            <Image source={require('../../assets/logo2.png')} style={styles.logoimage} />
          </TouchableOpacity>
          <TouchableOpacity onPress={()=> router.push('/mypage-hairstyle')}>
            <Image source={require('../../assets/mypage.png')} style = {styles.mypageimage}/>
          </TouchableOpacity>
        </View>
        <Text style ={{fontSize:20,marginTop:40,left:20}}>
            마이페이지
        </Text>

        <View style ={styles.profile}></View>
    
    {/* 마이페이지 카드 */}
    <View style={styles.profileCard}>
      <Image source={require('../../assets/profile.png')} style={styles.profileIcon} />
      <View>
        <Text style={styles.profileText}>사용자</Text>
        <Text style={styles.profileText}>남</Text>
        <Text style={styles.profileText}>서울시 강남구</Text>
      </View>
    </View>
    
    {/* 탭 버튼 */}
    <View style={styles.tabs}>
      <TouchableOpacity onPress={() => router.push('/mypage-hairstyle')}
        style ={styles.tabItem}>
        <Text style={[styles.tabText, pathname === '/mypage-hairstyle'&&styles.activeTab]}>Hairstyle</Text>
         {pathname === '/mypage-hairstyle' && <View style={styles.underline} />}
      </TouchableOpacity>
      <TouchableOpacity onPress={() => router.push('./mypage-hairshop')}
        style={styles.tabItem}>
        <Text style={[styles.tabText, pathname ==='mypage-hairshop' && styles.activeTab]}>Hairshop</Text>
        {pathname === '/mypage-hairshop' && <View style={styles.underline} />}
      </TouchableOpacity>
    </View>

    <View style={styles.divider} />
    <ScrollView contentContainerStyle={{ paddingBottom: 50 }}>
    {/* 샵 카드 리스트 */}
    {shops.map((shop) => (
      <View key={shop.id} style={styles.shopCard}>
        <Text style={styles.shopName}>{shop.name}</Text>
        <Text style={styles.shopDesc}>{shop.desc}</Text>
        <Text style={styles.shopDetail}>스타일: {shop.style}</Text>
        <Text style={styles.shopDetail}>위치: {shop.location}</Text>
        <Text style={styles.shopDetail}>tel:{shop.tel}</Text>
        <TouchableOpacity onPress ={()=> Linking.openURL('https://map.naver.com/p/search/%ED%95%98%EC%B8%A0%EB%8F%84%EC%82%B0/place/1710391167?c=15.00,0,0,0,dh&placePath=%3Fentry%253Dbmp')}>
                              <Text style={styles.link}>link</Text>
                            </TouchableOpacity> 
      </View>
    ))}
  </ScrollView>
</View>   
         
    
  );
}

const styles = StyleSheet.create({

  header:{
    height:55,
    flexDirection:'row',
    justifyContent : 'space-between',
    paddingHorizontal:15,
    alignItems : 'center',
    backgroundColor : '#FFBCC2'
  },
  logoimage: {
    width: 160,
    height: 45,
    resizeMode : 'contain',
  },
  mypageimage:{
    width :34,
    height : 33,
    resizeMode : 'contain',
  },

  profileCard: {
    backgroundColor: '#FFEFF1',
    borderRadius: 10,
    margin: 20,
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 20,
  },
  profileIcon: {
    width: 70,
    height: 70,
    resizeMode: 'contain',
    backgroundColor : '#FFFFFF',
    borderRadius : 10
  },
  profileText: {
    fontSize: 16,
    color: '#3F414E',
  },
  tabs: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 8,
    gap: 15,
  },
  tabText: {
    fontSize: 16,
    color: '#FF8994',
  },
  activeTab: {
   color: '#FF8994'
  },
  divider: {
    height: 1,
    backgroundColor: '#D9D9D9',
    marginHorizontal: 20,
    marginBottom: 10,
  },
  shopCard: {
    backgroundColor: '#FFE6E9',
    marginHorizontal: 20,
    marginBottom: 20,
    padding: 15,
    borderRadius: 10,
  },
  shopName: {
    fontWeight: 'bold',
    fontSize: 16,
    marginBottom: 5,
    textAlign: 'center',
  },
  shopDesc: {
    fontSize: 14,
    marginBottom: 5,
    textAlign: 'center',
  },
  shopDetail: {
    fontSize: 12,
    color: '#3F414E',
    textAlign: 'center',
  },
  link: {
    textAlign: 'center',
    color: '#FFBCC2',
    marginTop: 5,
    fontWeight: 'bold',
  },
  underline:{
    marginTop:3,
    top:8,
    height: 2,
    width: '100%',
    backgroundColor: '#CCCCCC',
    
  },
  tabItem:{
  alignItems: 'center',
  paddingHorizontal: 12,
  }
});

