import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import Checkbox from 'expo-checkbox';

export default function DiscoverSurvey() {
  const router = useRouter();
  const [selectedTab , setselectedTab] = useState('DISCOVER');
  const [selectedGender, setSelectedGender] = useState(null);
  const [selectedHairType, setSelectedHairtype] = useState(null);
  const [selectedHairLength, setSelectedHairLength] = useState(null);

  const handleSelect = (value,current,setter) => {
    if(current === value) {
        setter(null);
    }else {
        setter(value);
    }

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
        <Text style = {styles.text}>최적의 헤어스타일을 찾기 위한{'\n'}
                            설문을 진행합니다.</Text>
        <Text>{'\n'}</Text>
        <Text>{'\n'}</Text>
        <View style={[styles.line]}/>
        <View style ={styles.container}>
            {/*성별 질문*/}
           <View style = {styles.questionBlock1}>
            <Text style ={styles.question}>당신의 성별은 무엇인가요?</Text>
            <View style={styles.optionsRow}>
                {['남성', '여성'].map((option) => (
                    <TouchableOpacity
                        key={option}
                        style ={styles.optionItem}
                        onPress={() => handleSelect(option, selectedGender, setSelectedGender)}>
                    <Checkbox
                        value={selectedGender === option}
                        color={selectedGender === option ? '#FFBCC2' : undefined}
                        style={styles.checkbox}/>
                    <Text style={styles.optionText}>{option}</Text>
                    </TouchableOpacity>
            ))}
            </View>
           </View>
           <View style={[styles.line]}/>
            {/* 모발 질문 */}
           <View style = {styles.questionBlock2}>
             <Text style ={styles.question}>당신의 모발 유형을 알려주세요.</Text>
             <View style = {styles.optionsRow}>
                {['직모', '곱슬', '반곱슬'].map((option) => (
                    <TouchableOpacity
                        key={option}
                        style={styles.optionItem}
                        onPress={() => handleSelect(option, selectedHairType, setSelectedHairtype)}>
                    <Checkbox
                        value={selectedHairType === option}
                        color={selectedHairType === option ? '#FFBCC2' : undefined}
                        style={styles.checkbox}/>
                    <Text style={styles.optionText}>{option}</Text>
                    </TouchableOpacity>
                ))}
             </View>
           </View> 
           <View style={[styles.line]}/>
            {/* 기장 질문 */}
          <View style = {styles.questionBlock3}> 
            <Text style={styles.question}>당신의 현재 헤어 기장을 알려주세요.</Text>
            <View style ={styles.optionsRow}>
                {['단발', '중단발', '장발'].map((option) => (
                    <TouchableOpacity
                        key={option}
                        style = {styles.optionItem}
                        onPress={() => handleSelect(option, selectedHairLength, setSelectedHairLength)}>
                    <Checkbox
                        value={selectedHairLength === option}
                        color={selectedHairLength === option ? '#FFBCC2' : undefined}
                        style={styles.checkbox}
                        />
                    <Text style={styles.optionText}>{option}</Text>    
                    </TouchableOpacity>
                ))}
            </View>
           </View>
        </View>
        <TouchableOpacity onPress={() => router.push('/discover-camera')} style={styles.selectedButton}>
                <View style={styles.selectedButtonContent}>
                  <Text style={styles.selectedButtonText}>SELECT IMAGE</Text>
                </View>
              </TouchableOpacity>
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
    fontSize : 18,
    fontWeight : 400,
    textAlign : 'center',
    top:20
  },
  selectedButton: {
    backgroundColor:'#FFBCC2',
    paddingVertical: 17,
    paddingHorizontal: 100,
    borderRadius: 10,
    marginTop: 30,
    marginHorizontal:30 ,
    alignItems:'center',  
    bottom: 40
  },
  selectedButtonText:{
    fontSize : 14,
    fontWeight:400,
    color :'#F6F1FB',
  },
  selectedButtonContent: {
    alignItems: 'center',
    flexDirection: 'row'
  },
  line :{
    width : 340,
    backgroundColor : '#B7B7B7',
    height:1,
    alignSelf : 'center',
    marginVertical:0.5,
  },
  container: {
    flex: 1,
    backgroundColor: 'white',
    padding: 24,
    justifyContent: 'center',
  },
  questionBlock1: {
    marginTop:10,       
    paddingHorizontal: 16,  
    alignItems: 'center',
  },
  questionBlock2: {
    marginTop : 10,
    marginBottom: 5,       
    paddingHorizontal: 16,  
    alignItems: 'center',
  },
  questionBlock3: {
    marginTop : 15,
    marginBottom: 5,       
    paddingHorizontal: 16,  
    alignItems: 'center',
  },
  question: {
    fontSize: 16,
    fontWeight: '400',
    marginTop: 15,
    marginBottom:10 ,
    color: '#3F414E',
    textAlign: 'center',
  },
  optionsRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    flexWrap: 'wrap',
    marginBottom: 15,
  },
  optionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginHorizontal: 10,
    marginVertical: 5,
    padding:7,
  },
  checkbox: {
    width: 20,
    height: 20,
    borderRadius: 10,
    marginRight: 8,
  },
  optionText: {
    fontSize: 14,
    color: '#3F414E',
  },
});


