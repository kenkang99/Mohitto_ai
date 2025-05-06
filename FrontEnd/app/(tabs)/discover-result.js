import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';

export default function DiscoverResult() {
  const router = useRouter();
  const [selectedTab , setselectedTab] = useState('DISCOVER');

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
        <Text style = {styles.text}>얼굴형 분석을 완료했습니다.</Text>
        
        <View style={styles.imageContainer}>
          <Image source={require('../../assets/example_result.png')}style ={styles.exampleImage}/>
          <View style={styles.outlineSqure}>
          </View>
        </View>
        

        <Text style = {styles.resultText}>
          얼굴형 : 달걀형 {'\n'}
          피부톤 : ##43566{'\n'}
          성별 : 남성
        </Text>
        <TouchableOpacity onPress={()=>router.push('./discover-recomendation')} style={styles.startButton}>
                <View style={styles.startButtonContent}>
                  <Text style={styles.startButtonText}>추천 받기</Text>
                </View>
              </TouchableOpacity>
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
    top:20
  },
  imageContainer :{
    width:'90%',
    height:300,
    top : 30,
    borderColor:'#FFBCC2',
    borderWidth:2,
    justifyContent : 'center',
    alignItems : 'center',
    alignSelf :'center',
    marginVertical : 20,
    position:'relative'
  },
  exampleImage :{
    resizeMode : 'cover',
    width : '100%',
    height : '100%',
  },
  startButton: {
    width:'90%',
    backgroundColor:'#FFBCC2',
    paddingVertical: 17,
    paddingHorizontal: 100,
    borderRadius: 10,
    marginTop: 30,
    marginHorizontal:30 ,
    alignItems:'center'  
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
  resultText : {
    textAlign : 'center',
    marginTop : 45,
    fontSize : 16,
  },
  outlineSqure :{
    borderColor:'#FF0101',
    width : 180,
    height : 258,
    borderWidth:1,
    position : 'absolute'
  }
});
