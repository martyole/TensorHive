<template>
  <section class="content">
    <v-alert
      v-model="alert"
      dismissible
      type="error"
    >
      {{ errorMessage }}
    </v-alert>
    <v-alert
      v-model="created"
      dismissible
      type="info"
    >
      {{ infoMessage }}
    </v-alert>
    <div class="data_table">
      <UsersInfo class="data_box" @createdUser="userCreatedAlert" @usersList="updateUsers" />
      <GroupsInfo class="data_box" :usersList="this.users" @createdGroup="groupCreatedAlert"/>
    </div>
  </section>
</template>

<script>
// import api from '../../api'
import moment from 'moment'
import GroupsInfo from './users_overview/GroupsInfo.vue'
import UsersInfo from './users_overview/UsersInfo.vue'
export default {
  components: {
    GroupsInfo,
    UsersInfo
  },
  data () {
    return {
      errorMessage: '',
      infoMessage: '',
      createdGroup: false,
      created: false,
      alert: false,
      users: []
    }
  },
  prettyDate (date) {
    if (date !== null) {
      return moment(date).format('dddd, MMMM Do, HH:mm')
    } else {
      return null
    }
  },
  methods: {
    groupCreatedAlert (value) {
      this.created = value
      this.infoMessage = 'Group created successfully'
    },
    userCreatedAlert (value) {
      this.created = value
      this.infoMessage = 'User created successfully'
    },
    updateUsers (value) {
      this.users = value
    }
  }
}
</script>

<style>
.float-right-button {
  float: right;
}
.input-group {
  padding-bottom: 2em;
  height: 4em;
  width: 100%;
}

.input-group span.input-group-addon {
  width: 2em;
  height: 4em;
}

@media (max-width: 1241px) {
  .input-group input {
    height: 4em;
  }
}
@media (min-width: 1242px) {
  .input-group input {
    height: 6em;
  }
}

.input-group-addon i {
  height: 15px;
  width: 15px;
}

.data_table{
  display: flex;
  flex-wrap: wrap;
}

.data_box{
  width: 45vw;
  margin-left: 1vh;
}
</style>
