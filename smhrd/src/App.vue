<template>
  <div id="header">
    <div id="backward">
      <button id="back" @click="goBack"><i class="fa-solid fa-arrow-left fa-2x"></i></button>
    </div>
        <div id="nav">
          <router-link to="/detected" id="detected">Detected</router-link>
          <router-link to="/" id="all">All patients</router-link>
          <div id="line"></div>
        </div>
            <div id="wrap-time">
              <div id="search">
                <span id="search-glass"><i class="fa-solid fa-magnifying-glass"></i></span>
                <input type="search" id="searchbox" placeholder="환자 ID or 이름 검색" v-model="searchQuery" @input="onSearch">
                <button type="button" @click="onSearch" id="src-btn">검색</button>
              </div>
              <div id="time">
                {{ currentTime }}
              </div>
          </div>
  </div>
  <hr>
<router-view/>
</template>

<script>
import { thisTypeAnnotation, throwStatement } from '@babel/types'
import moment from 'moment';
import axios from 'axios';
import sha512 from 'js-sha512';
import bcrypt from 'bcryptjs';
export default {
  data () {
    return {
      currentTime: '',
      searchQuery: '',
      ipAddress: '',
      id: '',
      password: '',
      encryptedId: '',
      encryptedPassword: '',
      encryptedIP:'localhost',
      defaultCredentials: {
        user_id: 'user1',
        password: 'password1',
        IP:'http://127.0.0.1'
      },
      salt:'',
      token:'',
      sepsisPatient:[],
      initialLoad: true
    }
  },
  async created(){
    this.url = this.$route.path;
    await this.loadToken();
    if (this.$store.state.sepsisPatient.lenth==0){
      this.loadSepsisPatient();
    }
  },
  watch: {
    '$store.state.sepsisPatient': {
      deep: true,
      handler: function(newVal, oldVal) {
        console.log('Watch handler 실행됨');
        console.log('sepsisPatient 변경됨:', newVal, oldVal);
        if (this.initialLoad) {
        this.initialLoad = false;
        return;
      }

      newVal = Array.isArray(newVal) ? newVal : [];
      oldVal = Array.isArray(oldVal) ? oldVal : [];

      const addedPatients = newVal.filter(patient => !oldVal.some(oldPatient => oldPatient.pid === patient.pid));
      const removedPatients = oldVal.filter(patient => !newVal.some(newPatient => newPatient.pid === patient.pid));
      addedPatients.forEach(patient => {
        console.log(patient);
        this.$swal.fire({
            icon: 'success',
            title: `pid '${patient.pid}'번 '${patient.name}' 환자가 패혈증 환자에 추가되었습니다.`,
            timer: 3000,
            showConfirmButton: false,
        });
      });

      removedPatients.forEach(patient => {
        console.log(patient);
        this.$swal.fire({
            icon: 'info',
            title: `pid '${patient.pid}'번 '${patient.name}' 환자가 패혈증 환자에서 제외 되었습니다.`,
            timer: 3000,
            showConfirmButton: false,
            });
        });
    }
      }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    onSearch() {
      // store에 searchQuery 저장
      this.$store.dispatch('setSearchQuery', this.searchQuery);
  },
    async loadSepsisPatient(){
      const sepsis_raw=await axios.get("http://127.0.0.1:8002/api/sepsis_list_for_alarm");
      this.sepsisPatient=sepsis_raw.data.name_list;
      this.$store.dispatch('setSepsisPatient',this.sepsisPatient);
    },
    async loadToken() {
      let storedToken;
      if (!sessionStorage.getItem('storedToken')) {
        this.cryption();
      } else {
        // 토큰이 이미 localStorage에 있다면, 스토어에 저장하거나 필요한 작업을 수행합니다.
        storedToken=sessionStorage.getItem('storedToken');
        this.$store.dispatch('setToken', storedToken);
      }
    },
    async cryption(){
      const config = { 
        headers: { 
          'Content-Type': 'application/json'
        }
      };
      // const salt = await bcrypt.genSalt(10); // 10자리 salt 생성
      const hashedId=sha512(this.defaultCredentials.user_id);
      const user_raw= await axios.get("http://127.0.0.1:8002/api/get_salt/");
      this.salt=user_raw.data.salt;
      const hashedPassword = await bcrypt.hash(this.defaultCredentials.password,this.salt);
      const hashedIP=sha512(this.defaultCredentials.IP);
      const User={
        "user_id":hashedId,
        "password":hashedPassword,
        "IP":hashedIP,
        "salt":this.salt
      };
      const token_raw=await axios.post("http://127.0.0.1:8002/api/mk_token",User);
      this.token=token_raw.data.token;
      sessionStorage.setItem('storedToken', this.token);
      this.$store.dispatch('setToken', this.token);
      console.log(this.token);
    },
  },
  mounted () {
    this.moment = moment // moment 함수를 this에 할당합니다.

    this.timer = setInterval(() => {
      this.currentTime = this.moment().format('YYYY년 MM월 DD일 HH:mm:ss')
    }, 1000)
  },
  beforeUnmount () {
    clearInterval(this.timer);
  },
}

</script>

<style scoped>
@import "./assets/App.css";
</style>