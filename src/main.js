import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import store from './store'
// import VueRouter from 'vue-router';
import router from './router';
import "./index.css";

loadFonts()


let app = createApp(App);
app.use(vuetify)
app.use(store)
app.use(router)
    // global variables are defined in main.js
app.config.globalProperties.SERVERURL = "http://127.0.0.1:5000";

// app.use(VueRouter)
app.mount("#app");

require('./assets/scss/app.scss')