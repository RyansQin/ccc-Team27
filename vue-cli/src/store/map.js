;
import colors from '../data/color';
import { init } from 'echarts';
const state = {

    colors: []
};
const mutations = {
    

    'SET_COLOR' (state, colors){
        state.colors = colors;
    }
};
const actions = {

    initColors: ({commit}) => {
        commit('SET_COLOR',colors);

    }

};
const getters = {

    getAllColors: state => {
        return state.colors;
    }
};

export default{
    state,
    mutations,
    actions,
    getters
};