import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';

export default function HomeDiscover() {
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
            <TouchableOpacity key={tab} 
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
        <Text style = {styles.text}>얼굴형을 분석하고{'\n'}
                                    {'\n'}
                            최적의 헤어스타일을 탐색해보세요!
        </Text>
        <View style={styles.imageContainer}>
          <Image source={require('../../assets/example.png')}style ={styles.exampleImage}/>
          {/* 선 1 */}
          <View style = {[styles.line,{
            top:140,
            right : 60,
          }]}>
          </View>
          {/* 선 2 */}
          <View style = {[styles.line,{
            top:163,
            left : 161,
            transform : [{rotate:'-50deg'}],
          }]}>
          </View>

          {/* 점 1 */}
          <View style = {[styles.dot,{
            top:185,
            left : 165,
          }]}>
          </View> 
          {/* 선 3 */}
          <View style = {[styles.line,{
            top:110,
            left : 10,
          }]}>
          </View>
          {/* 선 4 */}
          <View style = {[styles.line2,{
            top:125,
            left : 62,
            transform : [{rotate:'50deg'}],
          }]}>
          </View>
          {/* 점 2 */}
          <View style = {[styles.dot,{
            top:136,
            left : 90,
          }]}>
          </View>
        </View>
        <TouchableOpacity onPress={()=>router.push('./discover-survey')} style={styles.startButton}>
                <View style={styles.startButtonContent}>
                  <Text style={styles.startButtonText}>GET STARTED</Text>
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
    top:29,
    resizeMode : 'cover',
    width : 200,
    height : 300,
  },
  startButton: {
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
  line:{
    position:'absolute',
    width : 60,
    height :2,
    backgroundColor:'white'
  },
  line2:{
    position:'absolute',
    width : 40,
    height :2,
    backgroundColor:'white'
  },
dot : {
  position:'absolute',
  width : 8,
  height : 8,
  borderRadius : 4,
  backgroundColor:'white',
},
});
