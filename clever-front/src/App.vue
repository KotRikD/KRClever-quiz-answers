<template>
  <div id="app">
    <div class="center" >
      <div class="container" v-if="questions.length > 0">
        <div class="card p-s" v-for="x in questions.slice().reverse()">
          <p class="t-l">Вопрос №{{ x['number'] }}: {{ x['question'] }}</p>
          <template v-if="x['correct_answer'] == 0">
            <div v-bind:class="[x['answer'] == 1 ? 'card p r-answer' : 'card p']">
              <p class="t-c">{{ x['answers']['first'][0] }} {{ x['answers']['first'][1] }}%</p>
            </div>
            <div v-bind:class="[x['answer'] == 2 ? 'card p r-answer' : 'card p']">
              <p class="t-c">{{ x['answers']['second'][0] }} {{ x['answers']['second'][1] }}%</p>
            </div>
            <div v-bind:class="[x['answer'] == 3 ? 'card p r-answer' : 'card p']">
              <p class="t-c">{{ x['answers']['third'][0] }} {{ x['answers']['third'][1] }}%</p>
            </div>
          </template>
          <template v-if="x['correct_answer'] != 0">
            <div v-bind:class="[x['correct_answer'] != 1 && x['answer'] != 1 ? 'card p' : x['correct_answer'] == 1 & x['answer'] == 1 || x['correct_answer'] == 1 ? 'card p r-answer' : 'card p nr-answer']">
              <p class="t-c">{{ x['answers']['first'][0] }} {{ x['answers']['first'][1] }}%</p>
            </div>
            <div v-bind:class="[x['correct_answer'] != 2 && x['answer'] != 2 ? 'card p' : x['correct_answer'] == 2 & x['answer'] == 2 || x['correct_answer'] == 2 ? 'card p r-answer' : 'card p nr-answer']">
              <p class="t-c">{{ x['answers']['second'][0] }} {{ x['answers']['second'][1] }}%</p>
            </div>
            <div v-bind:class="[x['correct_answer'] != 3 && x['answer'] != 3 ? 'card p' : x['correct_answer'] == 3 & x['answer'] == 3 || x['correct_answer'] == 3 ? 'card p r-answer' : 'card p nr-answer']">
              <p class="t-c">{{ x['answers']['third'][0] }} {{ x['answers']['third'][1] }}%</p>
            </div>
          </template>
        </div>
      </div>

      <div class="card" v-if="questions.length < 1" >
        <p class="bold">Привет!</p>
        Ожидай появления вопросов, они должны вот-вот появиться.</br></br>

        <span class="t-l" v-if="prize">
          Игра начнётся {{ timestamp }}</br>
          Призовой фонд: {{ prize }}₽
        </span>

        <p class="t-l">
          Сайт by <a href="https://kotrik.ru">KotRik</a><br>
          Скрипт для поиска by <a href="https://vk.com/idfelya">AdminFelix</a>
        </p>
      </div>
    </div>
  </div>
</template>
<script>
var firebase = require('firebase');
var moment = require('moment');

export default {
  name: 'app',
  data () {
    return {
      msg: 'KRClever FrontEnd',
      questions: [],
      prize: 0,
      timestamp: ''
    }
  },
  mounted() {  
      var app = firebase.initializeApp({
          apiKey: "lololololololololololololololloiloloololol;lokhjgjkhgvbhjfgcv",
          authDomain: "krclever-c002c.firebaseapp.com",
          databaseURL: "https://krclever-c002c.firebaseio.com",
          projectId: "krclever-c002c"
      });
      moment.locale('ru')
      this.listenData()
  },
  methods: {
    add(object) {
      this.questions.push(object)
      console.log(this.questions)
    },
    listenData() {
      firebase.database().ref("questions").on('value', (snapshot) => {
          var r = snapshot.val()
          if (r['now_question'] && r['now_question']['correct_answer'] != 0 && this.questions.length > 0) {
            this.questions[this.questions.length-1]['correct_answer'] = r['now_question']['correct_answer']
          } else if (r['now_question']) {
            this.add(r['now_question'])
          }
      })
      firebase.database().ref("startdata").on('value', (snapshot) => {
          var r = snapshot.val()
          if (r) {
              this.prize = r['prize']
              this.timestamp = moment.unix(r['timestamp']).format("Do MMM YYYY в LT") 
          }
      })
    } 
  },
    metaInfo: {
        title: 'KRClever - ответы для интеллектуальной игры Клевер',
        meta: [
            {property: 'og:locale', content: 'ru_RU'},
            {property: 'og:title', content: 'KRClever - ответы для интеллектуальной игры Клевер'},
            {property: 'og:image', content: 'https://clever.kotrik.ru/assets/pg.jpg'},
            {property: 'og:description', content: 'Здесь мы предоставляем возможные ответы для Клевера. Они могут быть не точными! Не стоит об этом забывать.'},
            {property: 'og:type', content: 'website'},
            {property: 'twitter:card', content: 'summary'},
            {property: 'twitter:title', content: 'KRClever - ответы для интеллектуальной игры Клевер'},
            {property: 'twitter:description', content: 'Здесь мы предоставляем возможные ответы для Клевера. Они могут быть не точными! Не стоит об этом забывать.'},
            {property: 'twitter:image', content: 'https://clever.kotrik.ru/assets/pg.jpg'}
        ]
    }
}
</script>

<style>
@font-face {
  font-family: 'GoogleSans-Bold';
  src: url('/fonts/GoogleSans-Bold.ttf');
}
@font-face {
  font-family: 'GoogleSans-Regular';
  src: url('/fonts/GoogleSans-Regular.ttf');
}
* {
  font-family: 'GoogleSans-Regular';
}
body, html {
  background-image: url(/assets/bg.png);
  background-position: center center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;
  margin: 0;
  height: 100%;
  width: 100%;
}
#app {
  height: 100%;
  width: 100%;
}
.bold {
  font-family: 'GoogleSans-Bold';
  font-size: 24px;
}
.card {
  background: white;
  padding: 32px;
  margin-right: 8px;
  margin-left: 8px;
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0,0,0,.12), 0 1px 2px rgba(0,0,0,.24);
}
.p-s {
  padding: 8px;
}
.p {
  padding: 1px;
  margin-bottom: 8px;
}
.r-answer {
  color: white;
  background: limegreen;
}
.p > p {
  margin-top: 8px;
  margin-bottom: 8px;
}
.t-l {
  text-align: left;
}
.t-r {
  text-align: right;
}
.t-c {
  text-align: center;
}
span {
  display: block;
}
.center{
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  text-align: center;  
}
.container{
  height: 95%;
  width: 100%;
  padding: 1rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto ;
}
.container > .card {
  margin-top: 15px;
  margin-bottom: 15px;
}
.p-s > p.t-l {
  margin-left: 8px;
}
.nr-answer {
  background: #ff0068;
  color: white;
}
a {
  text-decoration: none;
  color: #4B2E88;
  font-family: 'GoogleSans-Bold'
}
</style>
