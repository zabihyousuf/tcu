<template >
  <v-app style="background-color: rgb(10, 10, 10)">
    <div>
      <TimerComponent></TimerComponent></div
  ></v-app>
</template>

<script>
import semver from "semver";
import axios from "axios";
import axiosRetry from "axios-retry";

const MIN_API_VERSION = "1.1.0";

import TimerComponent from "./components/TimerComponent.vue";

export default {
  name: "App",
  components: { TimerComponent },
  data() {
    return {
      appPath: "",
    };
  },
  mounted() {
    // eslint-disable-next-line no-debugger
    const client = axios.create({ baseURL: `${this.SERVERURL}` });
    client
      .get("/echo", {
        "axios-retry": {
          retries: 5,
          retryDelay: axiosRetry.exponentialDelay,
        },
      })
      .then((response) => {
        console.log(response.data);
        axios
          .get(`${this.SERVERURL}/api_version`)
          .then((response) => {
            if (
              semver.lte(
                semver.clean(MIN_API_VERSION),
                semver.clean(response.data)
              )
            ) {
              console.log("API version satisfied");
              axios
                .get(`${this.SERVERURL}/find-track-start-data`)
                .then((response) => {
                  console.log(response.data);
                })
                .catch((error) => {
                  console.error(error);
                });
            } else {
              alert("Invalid API version");
            }
          })
          .catch((error) => {
            console.error(error);
          });
      })
      .catch((error) => {
        console.error(error);
      });
  },
  created() {
    this.appPath = window.location.pathname;
  },
  methods: {
    temp() {},
    updateState() {
      console.log("Server side event recieved at", new Date());
    },
  },
};
</script>
