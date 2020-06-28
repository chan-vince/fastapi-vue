<template>
    <div class="columns">
        <div class="column is-full">
            <div class="level" style="margin-top: 30px">
                <p class="level-left title is-5">Main Partners</p>
                <b-button class="level-right" type="is-primary" outlined icon-left="plus">Add</b-button>
            </div>
            <div class="columns">
                <div class="column is-4" v-for="partner in main_partners" :key="partner.id">
                    <div class="card" style="margin-bottom: 20px">
                        <div class="card-content">
                            <p class="title is-6 level-left">
                                {{ `${partner.first_name} ${partner.last_name}, ${partner.job_title.title}`}}
                            </p>
                            <p class="content level-left">
                                {{ partner.email }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="level" style="margin-top: 60px">
                <p class="title is-5">Employees</p>
                <b-button class="level-right" type="is-primary" outlined icon-left="plus">Add</b-button>
            </div>
            <div class="card">
                <b-table
                    :data="employees"
                    :selected.sync="selected"
                    default-sort="first_name"
                    sortable>
                    <template slot-scope="props">
                        <b-table-column field="first_name" label="Name" sortable>
                            {{ `${props.row.first_name} ${props.row.last_name}`}}
                        </b-table-column>
                        <b-table-column field="email" label="Email" sortable>
                            {{ props.row.email }}
                        </b-table-column>
                        <b-table-column field="job_title.title" label="Job Title" sortable>
                            {{ props.row.job_title.title }}
                        </b-table-column>
                        <b-table-column field="professional_num" label="Professional ID" sortable>
                            {{ props.row.professional_num }}
                        </b-table-column>
                        <b-table-column field="it_portal_num" label="IT Portal ID" sortable>
                            {{ props.row.it_portal_num }}
                        </b-table-column>
                        <b-table-column field="desktop_num" label="Desktop ID" sortable>
                            {{ props.row.desktop_num }}
                        </b-table-column>
                        <b-table-column field="active" label="Active" sortable>
                            <template
                                v-if="props.row.active == true">
                                <b-icon icon="check"></b-icon>
                            </template>
                            <template
                                v-else>
                                <b-icon icon="close"></b-icon>
                            </template>
                        </b-table-column>
                    </template>
                </b-table>
            </div>
        </div>
    </div>
</template>

<script>
import {client} from '../api.js'
 

export default {
    name: 'GPEmployeesList',
    props: ["practice_id"],
    data () {
        return {
            employees: [],
            main_partners: [],
            selected: null,
        }
    },
    watch: {
        practice_id: function(practice_id) {
            this.practice_id = practice_id
            this.getEmployeesForPractice()
            this.getMainPartnersForPractice()
        }
    },
    created () {
    },
    methods: {
        getEmployeesForPractice(){
            client.get(`api/v1/employees/practice`, {params: {practice_id: this.practice_id} })
            .then(response => {
                this.employees = response.data["employees"]
            })
        },
        getMainPartnersForPractice(){
            client.get(`api/v1/employees/main_partners`, {params: {practice_id: this.practice_id} })
            .then(response => {
                this.main_partners = response.data
            })
        },
    }
}
</script>