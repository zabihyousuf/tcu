// import Vue from 'vue'
import { createStore } from 'vuex'
// import semver from "semver";
import axios from "axios";
// import axiosRetry from "axios-retry";

// Vue.use(Vuex)
export default createStore({
    state: {
        sessions: [],
        apiUrl: "http://localhost:5000",
        currentSession: {},
        accountExists: false,
        loading: false,
        accountChecked: false,
        errorOnPage: false,
        lapped: false,
        appPath: "",
        MIN_API_VERSION: "1.1.0",
        error: '',
        started: false,
        trackFound: false,
    },
    getters: {
        get(state) {
            return state;
        },
        getSesh(state) {
            return state.sessions;
        },
        getAccountChecked(state) {
            return state.accountChecked;
        }
    },
    mutations: {
        set(state, payload) {
            state[payload[0]] = payload[1];
        },
        addSesh(state, payload) {
            state.sessions.push(payload);
        }
    },
    actions: {
        async addSession({ commit, }, form) {
            commit('set', ['loading', true]);
            commit('set', ['errorOnPage', false]);
            axios.defaults.headers.post['Content-Type'] = 'application/json;charset=utf-8';
            axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

            var today = new Date();
            var dd = String(today.getDate()).padStart(2, '0');
            var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
            var yyyy = today.getFullYear();

            today = mm + '/' + dd + '/' + yyyy;
            var tempSesh = {
                sessionDate: today,
                laps: form.laps,
                fastestLap: form.fastestLap,
                avgLap: form.avgLap,
            }
            commit('addSesh', tempSesh);
            var path = `${this.state.apiUrl}/add`
                // var bodyFormData = new FormData();
                // bodyFormData.append('session', this.state.sessions);
            axios
                .post(path, { form: this.state.sessions })
                .then((response) => {
                    commit('set', ['sessions', []]);
                    console.log(response);
                    commit('set', ['loading', false]);
                })
                .catch(function(error) {
                    console.log(error);
                    commit('set', ['errorOnPage', true]);
                    commit('set', ['loading', false]);
                });
        },

        async getIfLapped({ commit, }) {
            commit('set', ['loading', true]);
            axios
                .get(`${this.state.apiUrl}/GetIfLapped`)
                .then((response) => {
                    commit('set', ['lapped', response.data.lapped]);
                    commit('set', ['loading', false]);
                    console.log(response);
                })
                .catch((error) => {
                    console.error(error);
                });
        }
    },
    modules: {}
})