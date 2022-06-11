<template style="background-color: rgb(10, 10, 10)">
  <v-container fluid fill-height fill-width class="ml-6 mr-6 mt-5" id="bg">
    <div id="clock">
      <v-row style="margin-right: 10%">
        <v-col cols="12">
          <div class="mb-n6" align="center">
            <div id="app_text" style="font-size: 4vw">
              Lap <strong style="font-size: 8vw">{{ lapNumber }}</strong>
            </div>
          </div>
        </v-col>
      </v-row>

      <v-row style="margin-right: 10%; " class="mt-5 mb-n9">
        <v-col>
          <div class="mt-n5">
            <span class="time mb-n9">{{ time }}</span>
          </div>
        </v-col>
      </v-row>

      <v-row class="mt-12" style="margin-right: 4%">
        <v-col cols="6" class="mt-n9" style="text-align: center">
        <v-row justify="center">
            <v-col cols="12">
              <v-card-title id="app_text" class=" mb-n5" style="font-size: 4vw"
              >Fastest Lap</v-card-title
            >
            </v-col>
            
          </v-row>
          <v-row>
            <v-col>
              <v-card-text style="font-size: 8vw"
              ><strong>{{ fastestLap }}</strong></v-card-text
            >
            </v-col>
          </v-row>
        </v-col>
        <v-col  cols="6" class="mt-n9" style="text-align: center">
          <v-row justify="center">
            <v-col cols="12">
              <v-card-title id="app_text" class="mb-n5" style="font-size: 4vw"
              >Average Lap</v-card-title
            >
            </v-col>
            
          </v-row>
          <v-row>
            <v-col>
              <v-card-text style="font-size: 8vw;"
                ><strong style="">{{ averageLap }}</strong></v-card-text
              >
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-btn
          x-large
          style="font-size: 4em"
          id="reset"
          color="error"
          text
          class="white--text"
          @click="reset('end')"
          >End Session</v-btn
        >
      </v-row>
    </div>
    Î
  </v-container>
</template>

<script>
export default {
  name: "TimerComponent",
  props: {
    // selectedTrack: {
    //   type: String,
    //   default: "",
    //   required: false,
    // },
  },
  data() {
    return {
      time: "00:00.000",
      laps: [],
      latestLap: "",
      snackbar: false,
      timeBegan: null,
      timeStopped: null,
      stoppedDuration: 0,
      started: null,
      running: false,
      fastestLap: "00:00.000",
      averageLap: "00:00.000",
      lapNumber: 1,
      previousLap: 1,
      timeElapsed: 0,
      getLapLocation: null,
      selectedTrack: "",
      temp: null,
    };
  },
  computed: {
    getError() {
      return this.$store.state.error;
    },
  },
  created() {
    this.seeIfSessionShouldStart();
  },
  methods: {
    seeIfSessionShouldStart() {
      if (!this.running) {
        this.$store.dispatch("getIfLapped");
        if (this.$store.state.lapped) {
          this.start();
          // this.$forceUpdate();
        } else {
          setTimeout(this.seeIfSessionShouldStart, 500);
        }
      }
    },
    start() {
      if (this.running) return;

      if (this.timeBegan === null) {
        this.reset();
        this.timeBegan = new Date();
      }

      if (this.timeStopped !== null) {
        this.stoppedDuration += new Date() - this.timeStopped;
      }

      this.started = setInterval(this.clockRunning, 10);
      this.running = true;
      this.temp = setInterval(this.callEverySecond, 250);
    },
    stop() {
      this.running = false;
      this.timeStopped = new Date();
      clearInterval(this.started);
      clearInterval(this.getLapLocation);
      clearInterval(this.temp);
    },
    reset(calledFrom) {
      if (calledFrom === "end") {
        if (this.lapNumber == 1) {
          this.laps.push({
            time: this.time,
            lap: this.lapNumber,
            timeDiff: this.timeElapsed.getTime(),
          });
          this.calcAvgAndFastest();
        }
        this.$store.dispatch("addSession", {
          laps: this.laps,
          fastestLap: this.fastestLap,
          avgLap: this.averageLap,
        });
        this.running = false;
        this.laps = [];
        clearInterval(this.started);
        clearInterval(this.getLapLocation);
        clearInterval(this.temp);

        this.stoppedDuration = 0;
        this.timeBegan = null;
        this.timeStopped = null;
        this.time = "00:00.000";
        this.lapNumber = 1;
        this.fastestLap = "00:00.000";
        this.averageLap = "00:00.000";
      } else if (calledFrom === "lap") {
        this.running = false;
        clearInterval(this.started);
        clearInterval(this.getLapLocation);
        clearInterval(this.temp);

        this.stoppedDuration = 0;
        this.timeBegan = null;
        this.timeStopped = null;
        this.time = "00:00.000";
      }
    },
    clockRunning() {
      var currentTime = new Date();
      this.timeElapsed = new Date(
        currentTime - this.timeBegan - this.stoppedDuration
      );
      var min = this.timeElapsed.getUTCMinutes();
      var sec = this.timeElapsed.getUTCSeconds();
      var ms = this.timeElapsed.getUTCMilliseconds();

      this.time =
        this.zeroPrefix(min, 2) +
        ":" +
        this.zeroPrefix(sec, 2) +
        "." +
        this.zeroPrefix(ms, 3);
    },
    zeroPrefix(num, digit) {
      var zero = "";
      for (var i = 0; i < digit; i++) {
        zero += "0";
      }
      return (zero + num).slice(-digit);
    },
    lap() {
      this.laps.push({
        time: this.time,
        lap: this.lapNumber,
        timeDiff: this.timeElapsed.getTime(),
      });
      this.lapNumber++;
      this.latestLap = this.time;
      this.calcAvgAndFastest();
      this.reset("lap");
      this.start();
    },
    calcAvgAndFastest() {
      var totalTime = 0;
      for (var i = 0; i < this.laps.length; i++) {
        totalTime += this.laps[i].timeDiff;
      }
      this.fastestLap = this.msToTime(
        Math.min(...this.laps.map((lap) => lap.timeDiff))
      );

      var tempAvgTime = totalTime / this.laps.length;
      this.averageLap = this.msToTime(tempAvgTime);
    },
    msToTime(duration) {
      var milliseconds = parseInt(duration % 1000),
        seconds = parseInt((duration / 1000) % 60),
        tempMinutes = parseInt((duration / (1000 * 60)) % 60),
        minutes = tempMinutes < 10 ? "0" + tempMinutes : tempMinutes;
      seconds = seconds < 10 ? "0" + seconds : seconds;

      return minutes + ":" + seconds + "." + milliseconds;
    },
    callEverySecond() {
      this.$store.dispatch("getIfLapped");
      if (this.$store.state.lapped === "true" && this.running) {
        this.lap();
      }
    },
  },
  beforeUnmount() {
    clearInterval(this.started);
    clearInterval(this.getLapLocation);
    clearInterval(this.temp);
  },
};
</script>
