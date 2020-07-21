<template>
    <div class="card">
        <div class="card-header-title" style="margin: 30px 75px 0px 10px">
            <p class="title is-3">
                General
            </p>
        </div>
        <div class="card-content">
            <section style="padding-right: 50px">
                <b-field label="Name" horizontal>
                    <b-input v-model="name" size="is-default" required
                             placeholder="Enter a GP Practice Name"></b-input>
                </b-field>
                <b-field label="National Code" horizontal>
                    <b-input v-model="national_code" size="is-default" required
                             placeholder="Enter a National Code"></b-input>
                </b-field>
                <b-field label="EMIS CDB Practice Code" horizontal>
                    <b-input v-model="emis_cdb_practice_code" size="is-default" required
                             placeholder="Enter a National Code"></b-input>
                </b-field>
                <b-field label="Go Live Date" horizontal>
                    <b-datepicker v-model="go_live_date"
                                  :first-day-of-week="1"
                                  placeholder="Click to select...">
                        <button class="button is-primary"
                                @click="go_live_date = new Date()">
                            <b-icon icon="calendar-today"></b-icon>
                            <span>Today</span>
                        </button>

                        <button class="button is-danger"
                                @click="go_live_date = null">
                            <b-icon icon="close"></b-icon>
                            <span>Clear</span>
                        </button>
                    </b-datepicker>
                </b-field>
                <br>
                <div class="field level-left" horizontal>
                    <b-checkbox v-model="closed"
                                type="is-primary">
                        Practice closed
                    </b-checkbox>
                </div>
                <div class="level" style="padding-top: 20px">
                    <b-field class="level-left">
                        <b-checkbox-button v-model="checkboxGroup" v-for="system in access_systems" :key="system.id"
                                           :native-value="system.name"
                                           type="is-success"
                                           v-on:input="printSelected">
                            <span>{{system.name}}</span>
                        </b-checkbox-button>
                    </b-field>

                    <div class="level-right" style="padding-top: 20px">
                        <b-button v-on:click="saveDetails" type="is-primary" outlined icon-left="content-save">Save
                        </b-button>
                    </div>
                </div>
            </section>
        </div>
    </div>
</template>

<script>
    import {client} from '../api.js'
    import isEqual from 'lodash.isequal';


    export default {
        name: 'GPDetailsGeneralForm',
        props: ['practice_details'],
        data() {
            const today = new Date()
            return {
                go_live_date: today,
                minDate: new Date(today.getFullYear(), today.getMonth(), today.getDate()),
                name: '',
                national_code: '',
                emis_cdb_practice_code: '',
                closed: false,
                access_systems: [],
                checkboxGroup: [],
                checkboxGroupInit: []
            }
        },
        watch: {
            practice_details: function (details) {
                this.id = details['id']
                this.name = details['name']
                this.national_code = details['national_code']
                this.emis_cdb_practice_code = details['emis_cdb_practice_code']
                this.go_live_date = new Date(details['go_live_date'])
                this.closed = details['closed']
                this.checkboxGroup = details['access_systems'].map((item) => item["name"])
                this.checkboxGroupInit = details['access_systems'].map((item) => item["name"])
            }
        },
        methods: {
            getAllAccessSystems() {
                client.get(`api/v1/access_system`)
                    .then(response => {
                        this.access_systems = response.data
                    })
            },
            printSelected() {
                console.log(this.checkboxGroup)
            },
            saveDetails() {
                let promises = [];
                let message = "No changes made";
                let type = "is-success";
                let gen_body = {
                    requestor_id: 5000,
                    target_table: "practices",
                    target_id: this.id,
                    link: false
                }
                let as_body = {
                    requestor_id: 5000,
                    target_table: "_association_practice_systems",
                    target_id: this.id,
                    link: true
                }
                let gen_payload = {
                    "name": this.name,
                    "national_code": this.national_code,
                    "emis_cdb_practice_code": this.emis_cdb_practice_code,
                    "go_live_date": this.go_live_date.toISOString().split('T')[0],
                    "closed": this.closed,
                }

                let access_system_ids = this.access_systems
                    .filter(i => this.checkboxGroup.includes(i.name))
                    .map(i => ({"practice_id": this.id, "item": i.id}))

                let as_payload = {
                    action: "add",
                    elements: access_system_ids,
                }

                gen_body.payload = gen_payload
                as_body.payload = as_payload


                promises.push(client.put(`api/v1/stagingbeta`, gen_body)
                    .then(response => {
                        if (response.status === 200) {
                            message = "Request submitted successfully"
                        }
                    })
                    .catch(function (error) {
                        console.log(error.response.data.detail);
                        message = 'Error saving GP General details'
                        type = 'is-danger'
                    }))

                if (!(isEqual(this.checkboxGroup, this.checkboxGroupInit))) {
                    console.log("Submitting access systems")
                    promises.push(client.put(`api/v1/stagingbeta/link`, as_body)
                        .then(response => {
                            if (response.status === 200) {
                                message = "Request submitted successfully"
                                type = "is-success";
                            }
                        })
                        .catch(function (error) {
                            console.log(error.response.data.detail);
                            message = 'Error saving Access Systems'
                            type = 'is-danger'
                        }))
                }

                Promise.all(promises).then(() => {
                    this.$buefy.toast.open({
                        message: message,
                        type: type
                    })
                    this.$emit('newRequestGenerated')
                })
            }
        },
        created() {
            this.access_systems = this.getAllAccessSystems()
        }
    }
</script>

<style scoped>
    .title {
        font-weight: lighter;
    }
</style>