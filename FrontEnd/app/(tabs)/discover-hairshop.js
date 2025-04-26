import React, { useState } from 'react';
import { Linking,View, Text, TouchableOpacity, Image, StyleSheet, ScrollView } from 'react-native';
import { useRouter, usePathname } from 'expo-router';
import MapView, {Marker} from 'react-native-maps';
import {Feather} from '@expo/vector-icons'

export default function DiscoverHairshop() {
  const router = useRouter();
  const pathname = usePathname();
  const [selectedTab , setselectedTab] = useState('HAIRSHOP');
  const [bookmarkedIds, setBookmarkedIds] = useState([]);
  
  
  const toggleBookmark = (id) =>{
    if (bookmarkedIds.includes(id)) {
      setBookmarkedIds(prev => prev.filter(item => item!==id));
    } else {
      setBookmarkedIds(prev => [...prev,id]);
    }
  };

  const mockLocations = [
  {
    id : 1,
    name : '하츠도산',
    latitude: 37.523387,
    longitude:127.035069,
  }

  ]
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

      <View style={{flex: 1}}>
        <View style={styles.buttonContainer}>
          
        {['DISCOVER','SIMULATION','HAIRSHOP'].map((tab)=>(
                    <TouchableOpacity 
                    key={tab}
                    onPress={() =>  {
                      setselectedTab(tab);
                      if (tab === 'DISCOVER') {
                        router.push('/home-discover');
                      } else if (tab === 'SIMULATION') {
                        router.push('/home-simulation');
                      } else {
                        router.push('/home-hairshop');
                      }
                    }}
                    style={styles.tabItem}>
                    <Text style={[styles.tabText,selectedTab === tab && styles.activeTabText]}>
                      {tab}
                    </Text>
                    {selectedTab === tab && <View style={styles.underline}/>}
                    </TouchableOpacity>))}  
                </View>
        <View style ={styles.horizontalLine}/>
        <Text style = {styles.text}>헤어스타일에 적합한 미용실을 추천합니다.</Text>
        <ScrollView contentContainerStyle ={{paddingBottom:50}}>
            <View style={styles.mapcontainer}>
              <MapView
                style = {{width:'100%',height:300}}
                initialRegion={{
                  latitude : 37.524460,
                  longitude : 127.035352,
                  latitudeDelta : 0.005,
                  longitudeDelta:0.005,}}>
                  {mockLocations.map((loc) =>(
                    <Marker
                      key = {loc.id}
                      coordinate={{ latitude: loc.latitude, longitude: loc.longitude }}
                      title={loc.name}>
                    </Marker>
                  ))}
              </MapView>
            </View>
            {/* 샵 카드 리스트 */}
                {[1, 2].map((_, index) => (
                  <View key={index} style={styles.shopCard}>
                    <View style={{flexDirection:'row',alignItems:'center',alignSelf:'center'}}>
                      <Text style={[styles.shopName,{marginRight:4}]}>하츠도산</Text>
                      <TouchableOpacity onPress={()=> toggleBookmark(index)}>
                        <Feather 
                          name = {bookmarkedIds.includes(index) ? 'bookmark' : 'bookmark'}
                          size={24}
                          color={bookmarkedIds.includes(index) ? '#FFBCC2' : 'gray'}
                          style = {{marginTop:-20}}
                        />
                      </TouchableOpacity>
                    </View>
                    <Text style={styles.shopDesc}>세련된 분위기의 최신 트렌드를 반영한 서비스</Text>
                    <Text style={styles.shopDetail}>스타일: 리프컷, 드롭컷, 가일컷</Text>
                    <Text style={styles.shopDetail}>위치: 서울시 강남구 압구정동 189로</Text>
                    <Text style={styles.shopDetail}>tel: 02-1010-1010</Text>
                    <TouchableOpacity onPress ={()=> Linking.openURL('https://map.naver.com/p/search/%ED%95%98%EC%B8%A0%EB%8F%84%EC%82%B0/place/1710391167?c=15.00,0,0,0,dh&placePath=%3Fentry%253Dbmp')}>
                      <Text style={styles.link}>link</Text>
                    </TouchableOpacity> 
                  </View>
                ))}
        </ScrollView>
          </View>
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
  horizontalLine: {
    height: 1,               
    backgroundColor: '#B7B7B7', 
    width: '100%',          
    marginTop:0,
    bottom:5
  },
  buttonContainer :{
    flexDirection:'row',
    justifyContent : 'space-around',
    marginHorizontal : 20,
    marginTop : 15,
  },
  tabContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  tabItem: {
    alignItems: 'center',
    paddingBottom: 5,
    marginHorizontal :15
  },
  
  tabText: {
    fontSize: 14,
    color: '#3F414E',
    fontWeight: '400',
  },
  
  activeTabText: {
    fontWeight: 'bold',
  },
  
  underline: {
    marginTop: 15,
    height: 2,
    width: '100%',
    backgroundColor: '#A3A3A3',
  },
  text:{
    fontSize : 16,
    fontWeight : 400,
    textAlign : 'center',
    marginTop:30,
  },
  imageContainer :{
    width:330,
    height:350,
    top : 30,
    backgroundColor:'#FFE0E3',
    justifyContent : 'center',
    alignItems : 'center',
    alignSelf :'center',
    marginVertical : 20,
    borderRadius:20
  },
  exampleImage :{
    top:24.5,
    resizeMode : 'cover',
    width : 300,
    height : 300,
  },
  startButton: {
    backgroundColor:'#FFBCC2',
    paddingVertical: 17,
    paddingHorizontal: 100,
    borderRadius: 10,
    marginTop: 30,
    marginHorizontal:30 ,
    alignItems:'center',
    bottom:20
  },
  startButtonText:{
    fontSize : 14,
    fontWeight:400,
    color :'#F6F1FB',
    
  },
  startButtonContent: {
    alignItems: 'center',
    flexDirection: 'row'
  },
  mapcontainer:{
    borderColor:'#FFBCC2',
    borderWidth:4,
    width : '90%',
    height:318,
    alignItems:'center',
    justifyContent:'center',
    alignSelf:'center',
    marginTop:30
  },
  shopCard :{
    backgroundColor:'#FFEFF1',
    width:'90%',
    height:180,
    marginTop:40,
    borderRadius:15,
    padding:10,
  },
  shopName: {
    fontSize: 16,
    marginBottom: 20,
    textAlign: 'center',
  },
  shopDesc: {
    fontSize: 16,
    marginBottom: 20,
    textAlign: 'center',
  },
  shopDetail: {
    fontSize: 16,
    color: '#3F414E',
    textAlign: 'center',
  },
  link: {
    textAlign: 'center',
    color: '#FFBCC2',
    marginTop: 5,
    fontSize:17,
    fontWeight : 'bold'
  },
});
