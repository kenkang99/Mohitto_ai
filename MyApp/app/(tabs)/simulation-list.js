import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet, ScrollView ,FlatList, TextInput} from 'react-native';
import { useRouter } from 'expo-router';
import {Feather} from '@expo/vector-icons';



export default function SimulationList() {
  const router = useRouter();
  const [selectedTab , setselectedTab] = useState('SIMULATION');
  const [query,setQuery] = useState ('');
  
  const handleSearch = () => {
    console.log('검색실행:',query);
  };

  const hairStyles = [
    {
      id :1 ,
      title : '가일컷',
      image : require('../../assets/style_example.png'),
      desc:'시원하고 손질이 편한 \n 남성 맞춤형 헤어',
      simulationLink: './home-simulation',
      hairshopLink : './discover-recomendation'
    },
    {
      id :2,
      title : '드롭컷',
      image : require('../../assets/style_example.png'),
      desc:'시원하고 손질이 편한 \n 남성 맞춤형 헤어',
      simulationLink: './home-simulation',
      hairshopLink : './discover-recomendation'
    },
  ];

  const filteredStyles = hairStyles.filter(style => 
    style.title.toLowerCase().includes(query.toLowerCase())
  );

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

        <Text style = {styles.text}> 최신 인기 헤어를 확인하세요.</Text>
        <View style={styles.searchContainer}>
          <TextInput
            placeholder='search'
            style={styles.input}
            value={query}
            onChangeText={setQuery}
            onSubmitEditing={handleSearch}/>
          <TouchableOpacity onPress={handleSearch}
          style ={{
            backgroundColor:"#FFBCC2",
            marginHorizontal:-10,
            borderRadius:8}}>
            <Feather 
            name = 'search' 
            size={40} 
            color="#FFFFFF"
            />
          </TouchableOpacity>
        </View>
         <View style={styles.sortDropdownWrapper}>
          <TouchableOpacity
            style = {styles.sortDropdownButton}
            onPress = {() => setShowDropdown (prev => !prev)}        
          >
          <Text style = {styles.sortDropdownText}>{sortOption}</Text>    
          <Feather name='chevron-down' size ={16} color={'#B7B7B7'}></Feather>
          </TouchableOpacity>
                  
          {showDropdown && (
            <View style = {styles.dropdownList}>
              {['인기순','최신순']
                .filter(option => option!==sortOption)
                .map(option => (
                 <TouchableOpacity
                  key ={option}
                  onPress={()=> {
                  setSortOption(option);
                  setShowDropdown(false);
                  }}
                  >
                  <Text style = {styles.dropdownItem}>{option}</Text>
                  </TouchableOpacity>
                  ))}
                    </View>
                  )}
                </View>
        
        <ScrollView>
        {filteredStyles.map((style)=>(
           <View key ={style.id} style={styles.imageContainer}>
           <Text style={{textAlign:'center',fontSize:16,top:-40}}>{style.title}</Text>
           <Image source={style.image}style ={styles.exampleImage}/>
           <Text style = {{textAlign:'center',fontSize:16,bottom:-10}} > 
             {style.desc} 
           </Text>
           <View style={{flexDirection:'row', gap:70,bottom:-40}}>
             <TouchableOpacity onPress={()=>router.push(style.simulationLink)}>
             <Text style={{color:'#FFBCC2'}}>SIMULATION</Text>
             </TouchableOpacity>
             <TouchableOpacity onPress={()=>router.push(style.hairshopLink)}>
             <Text style={{color:'#FFBCC2'}}>HAIRSHOP</Text>
             </TouchableOpacity>
           </View>
           </View>
        ))}        
        </ScrollView>
        </View>
      </View>
    
  );
}

const styles = StyleSheet.create({
  header:{
    flex : 0.001,
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
    fontSize : 16,
    fontWeight : 400,
    textAlign : 'center',
    top:20
  },
  imageContainer :{
    width:330,
    height:413,
    marginTop:20,
    backgroundColor:'#FFE0E3',
    justifyContent : 'center',
    alignItems : 'center',
    alignSelf :'center',
    marginVertical : 20,
    borderRadius:15
  },
  exampleImage :{
    resizeMode : 'cover',
    width : 195,
    height : 219,
    borderColor : '#FFFFFF',
    borderWidth: 2,
    bottom:25
  },
  searchContainer:{
    marginTop:40,
    flexDirection:'row',
    alignContent:'center',
    paddingHorizontal:10,
    height:40,
    margin:20,
    borderColor:'#FFBCC2',
    borderWidth:1,
    borderRadius:8
  },
  input :{
   flex:1,
   paddingVertical:5,
   paddingHorizontal:10,
  },
  result: {
    paddingVertical: 10,
    fontSize: 16,
  },
  result: {
    paddingVertical: 10,
    fontSize: 16,
  },
  sortDropdownWrapper: {
    justifyContent : 'flex-end',
    flexDirection: 'row',
    paddingright:20,
    position:'relative'
  },
  sortDropdownButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 15,
    borderColor: '#B7B7B7',
    justifyContent: 'flex-end',
  },
  sortDropdownText: {
    fontSize: 15,
    fontWeight:'bold',
    color: '#B7B7B7',
  },
  dropdownList: {
    position: 'absolute',
    marginTop:20,
    right:18,
    backgroundColor: 'rgba(255,255,255,0.7)',
    borderColor: '#F2F2F2',
    borderRadius:8,
    zIndex: 999,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.08,
    shadowRadius: 3,
  },
  dropdownItem: {
    marginTop:4,
    paddingVertical: 8,
    paddingHorizontal: 12,
    fontSize: 15,
    fontWeight:'bold',
    color:'#B7B7B7',
  },
}
);
