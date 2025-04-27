import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet,Button } from 'react-native';
import { useRouter } from 'expo-router';
import {Feather} from '@expo/vector-icons'

export default function DiscoverRecomendation() {
  const router = useRouter();
  const [selectedTab , setselectedTab] = useState('DISCOVER');
  
  const [bookmarkedIds, setBookmarkedIds] = useState([]);
  
  const toggleBookmark = (step) =>{
    if (bookmarkedIds.includes(step)) {
      setBookmarkedIds(prev => prev.filter(item => item!==step));
    } else {
      setBookmarkedIds(prev => [...prev,step]);
    }

  };
  const [step, setStep] = useState(1);
  const totalPages=5;

  const goNext = () => {
    if (step < totalPages) setStep(step + 1);

  };
  const goPrev = () => {
    if (step > 1) setStep(step -1);
  };

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
          
          <Text style = {styles.text}>다음과 같은 헤어를 추천합니다.</Text>
          <Text style = {styles.styleText}>레이어드컷</Text>
          <View style={styles.imageContainer}>
            <Image source={require('../../assets/example_result2.png')}style ={styles.exampleImage}/>   
          </View>
          <TouchableOpacity onPress={()=> toggleBookmark(step)}>
                                    <Feather 
                                      name = {bookmarkedIds ? 'bookmark' : 'bookmark'}
                                      size={30}
                                      color={bookmarkedIds  ? '#FFBCC2' : 'gray'}
                                      style={{alignSelf:'flex-end',marginHorizontal:25,marginTop:-17}}
                                    />
                                  </TouchableOpacity>
          <Text style = {styles.resultText}>
          달걀형인 경우에 어울리는 헤어입니다.{'\n'}
          캐주얼하면서도 손질이 간단하여 추천합니다.{'\n'}
          피부 톤에 맞는 염색 색상으로는{'\n'}
          애쉬그레이, 딥레드를 추천 드립니다.
          </Text>
          <Text style={{color:'#FFBCC2',textAlign:'center',marginTop:10}}>hairshop</Text>
          <View style = {{alignItems : 'center'}}>
            <View style ={{flexDirection:'row',alignItems:'center',justifyContent:'space-between',width : 300}}>
              <TouchableOpacity onPress={goPrev} disabled={step ===1 }>
                <Feather
                  name = 'chevron-left'
                  size = {20}
                  color ={step ===1 ? '#ccc' : '#FFBC22'}/>
              </TouchableOpacity>
              <Text style = {{marginHorizontal : 20 , color:'#FFBCC2'}}>
                {step}/{totalPages}
              </Text>
              <TouchableOpacity onPress = {goNext} disabled= {step === totalPages}>
                <Feather
                  name = 'chevron-right'
                  size={20}
                  color = {step === totalPages ? '#ccc' : '#FFBCC2'}/>
              </TouchableOpacity>
            </View>
          </View>
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
  styleText:{
    textAlign:'center',
    fontSize : 24,
    marginTop:40
  },
  imageContainer :{
    width:330,
    height:300,
    marginTop : 15,
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
    width : 325,
    height : 300,
  },
  resultText : {
    textAlign : 'center',
    marginTop : 10,
    fontSize : 16,
  },
  outlineSqure :{
    borderColor:'#FF0101',
    width : 180,
    height : 258,
    borderWidth:1,
    position : 'absolute'
  },
  page:{
    flex:1,
    justifyContent:'center',
    alignItems : 'center',
  },
});
