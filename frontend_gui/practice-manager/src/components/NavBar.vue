<template>
    <div style="padding-left: 20px">
        <b-navbar spaced shadow>
            <template slot="brand">
                <b-navbar-item tag="router-link" :to="{ path: '/login' }" style="padding-right: 40px">
                    <img
                        src="../../public/logo.png"
                        alt="GP Data Access System"
                    >
                </b-navbar-item>
            </template>
            <template slot="start">
                <b-navbar-dropdown v-show="isAdmin" label="Practices" hoverable>
                    <b-navbar-item href="/practices">
                        View All Practices
                    </b-navbar-item>
                    <b-navbar-item href="#">
                        Add New Practice
                    </b-navbar-item>
                    <b-navbar-item href="#">
                        Edit Practice Details
                    </b-navbar-item>
                </b-navbar-dropdown>
                <b-navbar-dropdown v-show="isAdmin" label="Employees" hoverable>
                    <b-navbar-item href="#">
                        View All Employees
                    </b-navbar-item>
                    <b-navbar-item href="#">
                        Add New Employee
                    </b-navbar-item>
                    <b-navbar-item href="#">
                        Edit Employee Details
                    </b-navbar-item>
                </b-navbar-dropdown>
                <b-navbar-item v-show="isAdmin" href="/approvals">
                    Pending Approvals
                    <template v-if="pending_count > 0">
                        ({{pending_count}})
                    </template>
                </b-navbar-item>
            </template>

            <template slot="end">
                <b-navbar-dropdown label="Switch View" hoverable>
                    <router-link to='/login'><b-navbar-item>Login Page</b-navbar-item></router-link>
                    <router-link to='/practices'><b-navbar-item>Admin Practice View</b-navbar-item></router-link>
                    <router-link to='/practice'><b-navbar-item>GP User View</b-navbar-item></router-link>
                </b-navbar-dropdown>
                <!-- <b-navbar-item tag="div">
                    <div class="buttons">
                        <a class="button is-light">
                            Report Issue
                        </a>
                    </div>
                </b-navbar-item> -->
            </template>
        </b-navbar>
    </div>
</template>

<script>
import {client} from '../api.js'


export default {
    name: 'NavBar',
    computed: {
      isAdmin() {
        if( (this.$route.path == "/login" || this.$route.path == "/practice")) {
          return false
        } else {
          return true
        }
      }
    },
    data () {
        return {
            pending_count: 0
        }
    },
    created () {
        this.getPendingApprovalsCount()
    },
    methods: {
        getPendingApprovalsCount(){
            client.get(`api/v1/staging/practice/count/pending`)
            .then(response => {
                this.pending_count = response.data
            })
        },
    }
//   props: {
//     msg: String
//   }
}
</script>