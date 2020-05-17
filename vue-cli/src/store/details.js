import detail from '../data/detail';
const state = {
    
    covidRateForWA: {},
    covidRateForNT: {},
    covidRateForQ: {},
    covidRateForSA: {},
    covidRateForNSW: {},
    covidRateForACT: {},
    covidRateForV: {},
    covidRateForT: {},
    covidRate: {
        "covid":0,
        "total":0
    }

};
const mutations = {
    'INIT_COVIDRATE' (state, detail){
        state.covidRate = detail;
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
                break;
            case "Northern Territory":
                state.covidRateForNT = covidRate;
                state.covidRate = state.covidRateForNT;
                console.log("gengxin");
                console.log(state.covidRate);
                break;
            case "Queensland":
                state.covidRateForQ = covidRate;
                state.covidRate = state.covidRateForQ;
                break;
            case "South Australia":
                state.covidRateForSA = covidRate;
                state.covidRate = state.covidRateForSA;
                break;
            case "New South Wales":
                state.covidRateForNSW = covidRate;
                state.covidRate = state.covidRateForNSW;
                break;
            case  "Australian Capital Territory":
                state.covidRateForACT = covidRate;
                state.covidRate = state.covidRateForACT;
                break;
            case  "Victoria":
                state.covidRateForV = covidRate;
                state.covidRate = state.covidRateForV;
                break;
            case  "Tasmania":
                state.covidRateForT = covidRate;
                state.covidRate = state.covidRateForT;
                break;
        }
    }

};
const actions = {

    initCovidRate: ({commit}) => {
        commit('INIT_COVIDRATE',detail);
    },

    loadCovidRate: ({commit},covidRateInfo) => {
        commit('SET_COVIDRATE',covidRateInfo);
    },



};
const getters = {

    getCovidRate: state => {
        return state.covidRate;
    }
};

export default{
    state,
    mutations,
    actions,
    getters
}