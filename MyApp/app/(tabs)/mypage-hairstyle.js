import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet,ScrollView } from 'react-native';
import { useRouter, usePathname } from 'expo-router';


export default function MyPageHairstyle() {
  const router = useRouter();
  const pathname = usePathname();

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
    <View style ={styles.imageContainer}>
      <View style={styles.styleCard1}>
        <Image source={require('../../assets/style_example.png')} style={styles.styleImage1} />
        <Text style={{textAlign:'center'}}>가일컷</Text>
      </View>
      <View style={styles.styleCard1}>
        <Image source={require('../../assets/style_example.png')} style={styles.styleImage1} />
        <Text style={{textAlign:'center'}}>가일컷</Text>
      </View>
    </View>
    <View style ={styles.imageContainer}>
      <View style={styles.styleCard1}>
        <Image source={require('../../assets/style_example.png')} style={styles.styleImage1} />
        <Text style={{textAlign:'center'}}>가일컷</Text>
      </View>
      <View style={styles.styleCard1}>
        <Image source={require('../../assets/style_example.png')} style={styles.styleImage1} />
        <Text style={{textAlign:'center'}}>가일컷</Text>
      </View>
    </View>  
  </ScrollView>
</View>   
         
  );
}

const styles = StyleSheet.create({

  header:{
    flex : 0.05,
    flexDirection:'row',
    justifyContent : 'space-between',
    paddingHorizontal:40,
    paddingVertical:25.5,
    alignItems : 'center',
    backgroundColor : '#FFBCC2'
  },
  logoimage: {
    width: 167,
    height: 44,
    resizeMode : 'contain',
    left:-30,
  },
  mypageimage:{
    width :34,
    height : 33,
    resizeMode : 'contain',
    right : -1
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
    color: '#FF8994',
  },
  divider: {
    height: 1,
    backgroundColor: '#D9D9D9',
    marginHorizontal: 20,
    marginBottom: 10,
  },
  imageContainer:{
    flexDirection : 'row'
  },
  styleImage1:{
    width : 103,
    height : 106,
    alignSelf : 'center',
    marginBottom : 15
  },
  styleCard1: {
    backgroundColor: '#FFEEEF',
    marginHorizontal: 20,
    marginBottom: 20,
    padding: 15,
    borderRadius: 10,
    width : 152,
    height : 188
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

