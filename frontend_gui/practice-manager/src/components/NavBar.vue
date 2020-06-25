<template>
    <b-navbar>
        <template slot="brand">
            <b-navbar-item tag="router-link" :to="{ path: '/' }">
                <img
                    src="../../public/logo.png"
                    alt="Lightweight UI components for Vue.js based on Bulma"
                >
            </b-navbar-item>
        </template>
        <template slot="start">
            <b-navbar-item href="#">
                Home
            </b-navbar-item>
            <b-navbar-item href="#">
                Access Systems
            </b-navbar-item>
            <b-navbar-item href="#">
                Pending Approvals
            </b-navbar-item>
            <b-navbar-dropdown label="Practices">
                <b-navbar-item href="#">
                    Add New Practice
                </b-navbar-item>
                <b-navbar-item href="#">
                    Edit Practice Details
                </b-navbar-item>
            </b-navbar-dropdown>
            <b-navbar-dropdown label="Employees">
                <b-navbar-item href="#">
                    Add New Employee
                </b-navbar-item>
                <b-navbar-item href="#">
                    Edit Employee Details
                </b-navbar-item>
            </b-navbar-dropdown>
        </template>

        <template slot="end">
            <b-navbar-dropdown label="Switch View">
                <b-navbar-item href="#">
                    Admin
                </b-navbar-item>
                <b-navbar-item href="#">
                    GP Practice
                </b-navbar-item>
            </b-navbar-dropdown>
            <b-navbar-item tag="div">
                <div class="buttons">
                    <a class="button is-light">
                        Report Issue
                    </a>
                </div>
            </b-navbar-item>
        </template>
    </b-navbar>
</template>

<script>
export default {
  name: 'NavBar',
//   props: {
//     msg: String
//   }
}
</script>