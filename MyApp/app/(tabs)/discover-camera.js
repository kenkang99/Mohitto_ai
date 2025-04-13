import React, { useEffect, useRef, useState } from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet } from 'react-native';
import { useRouter , usePathname} from 'expo-router';
import {CameraView,useCameraPermissions} from 'expo-camera';


export default function DiscoverCamera() {
  const router = useRouter();
  const pathname = usePathname();
  const [selectedTab , setselectedTab] = useState('DISCOVER');
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef (null);
  const [photoUri, setPhotoUri] = useState(null);

  useEffect(()=>{
    requestPermission();
  },[]);
  
  
  const takePicture = async () => {
    if(cameraRef.current) {
      const photo = await cameraRef.current.takePictureAsync();
      console.log('사진 URI:',photo.uri); //백엔드 연동시 여기에 API요청
      setPhotoUri(photo.uri);
        }
  };

  if(!permission?.granted) {
    return <Text>카메라 권한이 필요합니다.</Text>
  }


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

        <View style={styles.cameraContainer}>
          <CameraView style ={{flex:1}} ref={cameraRef} facing='front'/>
        </View>
         <View style = {styles.controls}>
          <View style = {styles.previewBox}>
          {photoUri && (
            <Image source = {{uri:photoUri}} style = {styles.previewImage}/>
          )}
         </View>
        <TouchableOpacity style={styles.shutterOuter} onPress={takePicture}>
       
        </TouchableOpacity>
        </View>
        <Text style ={styles.text}>이마가 나오도록 사진을 찍어주세요.{'\n'}
              그림자가 지지 않도록 사진을 찍어주세요.
        </Text>
    </View>
  </View>
  );
}


const styles = StyleSheet.create({
  header:{
    flex : 0.05,
    flexDirection:'row',
    justifyContent : 'space-between',
    paddingHorizontal:40,
    paddingVertical:25,
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
    right:-35
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
    fontSize : 15,
    fontWeight : 400,
    textAlign : 'center',
    top:20
  },
  cameraContainer: {
    width: 369,
    height:400,
    aspectRatio: 3 / 4,
    alignSelf: 'center',
    marginTop: 15,
    borderWidth: 1,
    borderColor: '#B7B7B7',
  },
  camera: {
    flex: 1,
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'space-arround',
    alignSelf : 'center',
    alignItems: 'center',
    marginTop: 16,
  },
  previewBox: {
    width: 40,
    height: 40,
    backgroundColor: '#000000',
    overflow: 'hidden',
    borderColor:'#FFBCC2',
    borderWidth:4,
  },
  previewImage: {
    width: '100%',
    height: '100%',
  },
  shutterOuter: {
    width: 70,
    height: 70,
    backgroundColor: '#FFBCC2',
    borderRadius: 35,
    justifyContent: 'center',
    alignSelf: 'center',
    alignItems: 'center',
    borderColor:'#FCE3E6',
    borderWidth:3,
    marginHorizontal:100,
    left : -20
    
  },

 
});