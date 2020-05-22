
const state = {
    age:[],
    population: [],
    tourism: [],
    disease: [],


};
const mutations = {

    'SET_AGE' (state, age){
        state.age = age;
    },
    'SET_POPULATION' (state,population){
        state.population = population;
    },
    'SET_TOURISM' (state,tourism){
        state.tourism = tourism;
    },
    'SET_DISEASE' (state,disease){
        state.disease = disease;
    }

};
const actions = {
    loadDisease: ({commit},disease) =>{
        commit('SET_DISEASE',disease);
    },
    loadAge: ({commit},age) =>{
        commit('SET_AGE',age);
    },
    loadPopulation: ({commit},population)=>{
        commit('SET_POPULATION',population);
    },
    loadTourism:({commit},tourism) =>{
        commit('SET_TOURISM',tourism);
    }
};
const getters = {
    getDisease: state=>{
        return state.disease;
    },
    getAge: state =>{
        return state.age;
    },
    getPopulation: state => {
        return state.population;
    },
    getTourism: state =>{
        return state.tourism;
    }
};

export default{
    state,
    mutations,
    actions,
    getters
}