<template>
    <section class="content">
      <v-alert
      v-model="alert"
      dismissible
      type="error"
    >
      {{ errorMessage }}
    </v-alert>
        <v-dialog
        width="500px"
        v-model="showModalCreateGroup"
      >
      <v-card>
        <v-card-text>
            <v-btn
              class="float-right-button"
              flat
              icon
              color="black"
              @click="showModalCreateGroup=false"
            >
              <v-icon>close</v-icon>
            </v-btn>
            <span class="headline">Create new group</span>
          </v-card-text>
          <v-card-text>
            <form @submit.prevent="createGroup">
              <v-card-text>
                Group name
              </v-card-text>
              <div class="input-group">
                <span class="input-group-addon"><i class="fa fa-info"></i></span>
                <input
                  class="form-control"
                  name="modalGroupName"
                  placeholder="Group name"
                  type="text"
                  v-model="modalGroupName"
                >
              </div>
              <v-card-text>
              Group members
              </v-card-text>
              <v-autocomplete
                v-model="usersValue"
                :items="usersList"
                :multiple=true
                placeholder="Username"
                item-value="id"
                item-text="username"
                prepend-icon="fa-group"
              />
              <v-card-text>
              Permissions
              </v-card-text>
                <v-autocomplete
                v-model="permissionsValue"
                :items="permissions"
                :multiple=true
                placeholder="Permission name"
                item-value="id"
                prepend-icon="fa-check"
                />
                <div class="input-group">
                  <v-btn color="blue darken-1" flat block>Add permission</v-btn>
                </div>
              <v-alert
                v-model="modalAlert"
                dismissible
                type="error"
              >
                {{ errorMessage }}
              </v-alert>
              <v-btn
                color="success"
                type="submit"
              >
                Create
              </v-btn>
            </form>
          </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="showModalEditGroup"
      width="500px"
    >
      <v-card>
        <v-card-text>
          <v-btn
            class="float-right-button"
            flat
            icon
            color="black"
            @click="showModalEditGroup = false"
          >
            <v-icon>close</v-icon>
          </v-btn>
          <v-card-text>
              Edit group current group: {{currentGroup.name}}
          </v-card-text>
          <v-card-text>
              New group name
          </v-card-text>
          <div class="input-group">
                <span class="input-group-addon"><i class="fa fa-info"></i></span>
                <input
                  class="form-control"
                  name="modalGroupName"
                  placeholder="Group name"
                  type="text"
                  v-model="group.name"
                >
          </div>
          <v-card-text>
              Edit group members
          </v-card-text>
          <v-autocomplete
              v-model="currentGroup.users"
              :items="usersList"
              :multiple=true
              placeholder="Username"
              item-value="id"
              item-text="username"
              prepend-icon="fa-group"
            />
          <v-card-text>
            Edit group permissions
          </v-card-text>
          <v-autocomplete
              v-model="currentGroup.permissions"
              :items="permissions"
              :multiple=true
              placeholder="Permission name"
              item-value="id"
              item-text="name"
              prepend-icon="fa-group"
            />
          <v-alert
            v-model="modalAlert"
            dismissible
            type="error"
          >
            {{ errorMessage }}
          </v-alert>
          <v-btn
            color="blue darken-1"
            flat @click="updateGroup"
          >
            Edit
          </v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="showModalRemoveGroup"
      width="400"
    >
      <v-card>
        <v-card-text
          class="headline grey lighten-2"
          primary-title
        >
          <v-btn
            class="float-right-button"
            flat
            icon
            color="black"
            @click="showModalRemoveGroup= false"
          >
            <v-icon>close</v-icon>
          </v-btn>
          Do you want to remove this group?
        </v-card-text>
        <v-card-actions>
          <v-layout align-center justify-end>
            <v-btn
              color="success"
              round
              @click="removeGroup()"
            >
              Yes
            </v-btn>
          </v-layout>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <div>
      <div class="text-xs-center pt-2">
        <v-btn color="primary" @click="showModalCreateGroup=true">Create group</v-btn>
        Total: {{numGroups}}
      </div>
      <v-data-table
        :headers="groupHeaders"
        :items="groups"
        :pagination.sync="pagination"
        item-key="id"
        hide-actions
        class="elevation-1"
      >
        <template slot="items" slot-scope="props">
          <tr>
            <td>{{ props.item.id }}</td>
            <td>{{ props.item.name }}</td>
            <td>{{ prettyDate(props.item.createdAt) }}</td>
            <td>{{ props.item.users.length }}</td>
            <td>{{ props.item.permissions.length }}</td>
            <td>
              <v-icon
                small
                @click="editGroup(props.item)"
              >
                edit
              </v-icon>
              <v-icon
                small
                @click="showGroupConfirmationDialog(props.item.id)"
              >
                delete
              </v-icon>
            </td>
          </tr>
        </template>
      </v-data-table>
      <div class="text-xs-center pt-2">
        <v-pagination v-model="pagination.page" :length="pages"></v-pagination>
      </div>
    </div>
    </section>
</template>

<script>
// import api from '../../../api'
import UsersOverview from '../UsersOverview.vue'
export default {
  name: 'GroupsInfo',
  props: {
    usersList: Array
  },
  data () {
    return {
      pagination: {},
      groupHeaders: [
        { text: 'Group id', value: 'id' },
        { text: 'Group name', value: 'name' },
        { text: 'Created at', value: 'gorupCreated' },
        { text: 'Users', sortable: false },
        { text: 'Permissions', sortable: false },
        { text: 'Actions', sortable: false }
      ],
      groups: [
        {
          id: 100,
          name: 'test',
          users: [],
          permissions: []
        },
        {
          id: 101,
          name: 'test1',
          users: [],
          permissions: []
        }
      ],
      group: {
        id: -1,
        name: '',
        users: [],
        permissions: []
      },
      user: {},
      usersValue: [],
      permissionsValue: [],
      permissions: [],
      permission: {
        id: -1,
        name: '',
        starts: '',
        ends: '',
        global: false,
        days: '',
        hourStart: '',
        hourEnd: ''
      },
      showModalCreateGroup: false,
      showModalRemoveGroup: false,
      showModalEditGroup: false,
      modalGroupName: '',
      modalGroupUsers: [],
      tempGroupId: 1,
      groupId: -1,
      currentGroup: {},
      errorMessage: '',
      modalAlert: false,
      alert: false,
      created: false
    }
  },
  created () {
    this.prettyDate = UsersOverview.prettyDate
  },
  computed: {
    pages () {
      if (this.pagination.rowsPerPage == null ||
            this.pagination.totalItems == null
      ) return 0

      return Math.ceil(this.pagination.totalItems / this.pagination.rowsPerPage)
    },

    numGroups () {
      return this.groups.length
    }
  },
  methods: {
    createGroup () {
      const { modalGroupName } = this
      this.showModalCreateGroup = false
      this.created = true
      this.sendCreated()
      this.groups.push({'id': this.tempGroupId, 'name': modalGroupName, 'users': this.usersValue, 'permissions': []})
      this.tempGroupId += 1
      this.usersValue = []
      this.checkGroups()
    },

    editGroup: function (currentGroup) {
      this.showModalEditGroup = true
      this.group.id = currentGroup.id
      this.group.name = currentGroup.name
      this.group.users = currentGroup.users
      this.currentGroup = currentGroup
    },

    updateGroup: function () {
      const groupIndex = this.groups.findIndex(ele => this.group.id)
      if (this.group.name !== this.currentGroup.name && this.group.name !== '') {
        this.groups[groupIndex].name = this.group.name
      }
      if (this.group.users !== this.currentGroup.users) {
        this.groups[groupIndex].users = this.group.users
      }
      this.showModalEditGroup = false
      this.checkGroups()
    },

    removeGroup: function () {
      var groupId = this.groupId
      this.groups = this.groups.filter(
        function (ele) {
          return ele.id !== groupId
        }
      )
      this.showModalRemoveGroup = false
      this.checkGroups()
    },

    checkGroups: function () {
      this.pagination['totalItems'] = this.groups.length
      this.pagination['rowsPerPage'] = 30
    },

    showGroupConfirmationDialog (id) {
      this.groupId = id
      this.showModalRemoveGroup = true
    },

    sendCreated: function () {
      this.$emit('createdGroup', this.created)
    }
  },
  mounted () {
    this.checkGroups()
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
