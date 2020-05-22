import detail from '../data/detail';
import covidNumForNSW from '../data/covidNumForNSW';
import dateForMost from '../data/dateForMost';
import dateForNT from '../data/dateForNt';
import covidNumForACT from '../data/covidNumForACT';
import covidNumForNT from '../data/covidNumForNT';
import covidNumForQue from '../data/covidNumForQue';
import covidNumForSA from '../data/covidNumForSA';
import covidNumForTAS from '../data/covidNumForTAS';
import covidNumForVIC from '../data/covidNumForVIC';
import covidNumForWA from '../data/covidNumForWA';
import actionForACT from '../data/actionForACT';
import actionForNSW from '../data/actionForNSW';
import actionForNT from '../data/actionForNT';
import actionForQUE from '../data/actionsForQUE';
import actionForSA from '../data/actionForSA';
import actionForTAS from '../data/actionForTAS';
import actionForVIC from '../data/actionForVIC';
import actionForWA from '../data/actionForWA';
import states from '../data/states';
const state = {
    action:[],
    states:states,
    sentiment:{},
    covidNum: [],
    curve: {},
    dateForMost: dateForMost,
    dateForNT: dateForNT,
    date: [],
    covidRateForWA: {},
    covidRateForNT: {},
    covidRateForQ: {},
    covidRateForSA: {},
    covidRateForNSW: {},
    covidRateForACT: {},
    covidRateForV: {},
    covidRateForT: {},
    covidRate: {
        "covid":5,
        "total":10
    }

};
const mutations = {

    'INIT_COVIDRATE' (state, detail){
        state.covidRate = detail;
    },
    'INIT_CURVE' (state,detail){
        state.curve = detail;
    },
    'SET_SENTIMENT' (state, sentiment){
        state.sentiment = sentiment;
    },

    'SET_DATE' (state, location){
        if(location == "Northern Territory"){
            state.date = state.dateForNT;
        }else{
            state.date = state.dateForMost;
        }
        
        
    },
    'SET_CURVE' (state, curve){
        state.curve = curve;
    },
    'SET_COVIDRATE' (state, {covidRate, location}) {
        console.log("loadCovidRate test");
        console.log(location+ "location");
        console.log(covidRate);
        console.log(location=="Northern Territory");
        switch(location) {
            case "Western Australia":
                state.covidRateForWA = covidRate;
                state.covidRate = state.covidRateForWA;
                state.covidNum = covidNumForWA;
                state.action = actionForWA;
                break;
            case "Northern Territory":
                state.covidRateForNT = covidRate;
                state.covidRate = state.covidRateForNT;
                console.log("gengxin");
                console.log(state.covidRate);
                state.covidNum = covidNumForNT;
                state.action = actionForNT;
                break;
            case "Queensland":
                state.covidRateForQ = covidRate;
                state.covidRate = state.covidRateForQ;
                state.covidNum = covidNumForQue;
                state.action = actionForQUE;
                break;
            case "South Australia":
                state.covidRateForSA = covidRate;
                state.covidRate = state.covidRateForSA;
                state.covidNum = state.covidNumForSA;
                state.action = actionForSA;
                break;
            case "New South Wales":
                state.covidRateForNSW = covidRate;
                state.covidRate = state.covidRateForNSW;
                state.covidNum = state.covidNumForNSW;
                state.action = actionForNSW;
                break;
            case  "Australian Capital Territory":
                state.covidRateForACT = covidRate;
                state.covidRate = state.covidRateForACT;
                state.covidNum = covidNumForACT;
                state.action = actionForACT;
                break;
            case  "Victoria":
                state.covidRateForV = covidRate;
                state.covidRate = state.covidRateForV;
                state.covidNum = covidNumForVIC;
                state.action = actionForVIC;
                break;
            case  "Tasmania":
                state.covidRateForT = covidRate;
                state.covidRate = state.covidRateForT;
                state.covidNum = covidNumForTAS;
                state.action = actionForTAS;
                break;
        }
    }

};
const actions = {
    initCurve: ({commit}) => {
      commit('INIT_CURVE',detail)  
    },

    initCovidRate: ({commit}) => {
        commit('INIT_COVIDRATE',detail);
    },

    loadCovidRate: ({commit},covidRateInfo) => {
        commit('SET_COVIDRATE',covidRateInfo);
    },

    loadCurve: ({commit},curve) => {
        commit('SET_CURVE', curve);
    },

    loadDate: ({commit}, location) => {
        commit('SET_DATE', location);
    },
    loadSentiment: ({commit}, sentiment) => {
        commit('SET_SENTIMENT',sentiment);
    }



};
const getters = {
    getAction: state =>{
        return state.action;
    },
    getSentiment: state =>{
        return state.sentiment;
    },

    
    getDate: state => {
        return state.date;
    },

    getCovidRate: state => {
        return state.covidRate;
    },

    getCurve: state => {
        return state.curve;
    },

    getDailyCovid: state => {
        return state.covidNum;
    },
    getStates: state => {
        return state.states;
    }
};

export default{
    state,
    mutations,
    actions,
    getters
}