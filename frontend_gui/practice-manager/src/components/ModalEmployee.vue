<template>
    <div class="modal-card">
        <header class="modal-card-head">
            <p class="modal-card-title">{{action}} Employee</p>
        </header>
        <section class="modal-card-body">

            <b-field label="Name" horizontal>
                <b-input
                    :value="this.name"
                    v-model="name"
                    placeholder="Name(s)"
                    required>
                </b-input>
            </b-field>

            <b-field label="Email" horizontal>
                <b-input
                    :value="this.email"
                    v-model="email"
                    placeholder="Email"
                    required>
                </b-input>
            </b-field>

            <b-field label="Job Title" horizontal>
                <b-select :placeholder="this.job_title.title"
                v-model="title_id">
                    <option
                        v-for="title in job_titles"
                        :value="title.id"
                        :key="title.id">
                        {{ title.title }}
                    </option>
                </b-select>
            </b-field>

            <b-field label="Practice" horizontal>
                <b-autocomplete
                    v-model="practice_name"
                    :data="filteredPractices"
                    :placeholder="practice_name"
                    icon="magnify"
                    clearable
                    @select="option => selected = option">
                    <template slot="empty">No results found</template>
                </b-autocomplete>
            </b-field>

            <b-field label="Professional ID" horizontal>
                <b-input
                    :value="this.professional_num"
                    v-model="professional_num"
                    placeholder="Professional ID"
                    required>
                </b-input>
            </b-field>

            <b-field label="IT Portal ID" horizontal>
                <b-input
                    :value="this.it_portal_num"
                    v-model="it_portal_num"
                    placeholder="IT Portal ID">
                </b-input>
            </b-field>
            <b-field label="Desktop ID" horizontal>
                <b-input
                    :value="this.desktop_num"
                    v-model="desktop_num"
                    placeholder="Desktop ID">
                </b-input>
            </b-field>

            <b-field label="Active" horizontal>
                <b-switch :value="this.active"
                v-model="active"
                type="is-success">
                </b-switch>
            </b-field>

        </section>
        <footer class="modal-card-foot">
            <button class="button" type="button" @click="$parent.close()">Cancel</button>
            <button class="button is-primary" @click="saveDetails(rowObject)">Save</button>
        </footer>
    </div>
</template>


<script>
    import {client} from '../api.js'

    export default {
        name: 'ModalEmployee',
        props: ["rowObject", "jobTitles", "action"],
        components: {
            
        },
        data() {
            return {
                isComponentModalActive: false,
                job_titles: [],
                id: '',
                name: '',
                email: '',
                title_id: null,
                professional_num: null,
                it_portal_num: null,
                desktop_num: null,
                active: true,
                source_id: null,
                practice_name: '',
                all_practices: [],
                job_title: {"title": ""}
            }
        },
        computed: {
            filteredPractices() {
                return this.all_practices.filter((option) => {
                    return option
                        .toString()
                        .toLowerCase()
                        .indexOf(this.practice_name.toLowerCase()) >= 0
                })
            }
        },
        created () {
            this.getAllPracticeNames();
            if (this.$props.jobTitles == null) {
                client.get(`api/v1/job_titles`)
                .then(response => {
                    this.job_titles = response.data
                })
            }
            else{
                this.job_titles = this.$props.jobTitles
            }
            console.log(`Row object: ${this.rowObject}`)
            if (this.rowObject != null){
                console.log("!!!!!!!")
                this.id = this.rowObject.id
                this.name = this.rowObject.name,
                this.email = this.rowObject.email,
                this.title_id = this.rowObject.job_title.id,
                this.professional_num = this.rowObject.professional_num,
                this.it_portal_num = this.rowObject.it_portal_num,
                this.desktop_num = this.rowObject.desktop_num,
                this.active = this.rowObject.active
                this.source_id = this.rowObject.id
                this.practice_name = this.rowObject.practices[0].name
            }
        },
        methods: {
            getAllPracticeNames() {
                client.get(`api/v1/practice/names`)
                .then(response => {
                    this.all_practices = response.data.names;
                })
                .catch( function(error) {
                    console.log(error)
                })
            },
            saveDetails() {
                var current = this;
                var payload = {
                    "id": this.id,
                    "name": this.name,
                    "email": this.email,
                    "job_title_id": this.title_id,
                    "professional_num": this.professional_num,
                    "it_portal_num": this.it_portal_num,
                    "desktop_num": this.desktop_num,
                    "active": this.active,
                    "source_id": this.source_id,
                    "practice_name": this.practice_name,
                    "requestor_id": 5000
                }
                if(self.action == "Add"){
                    client.post(`api/v1/staging/employee`, payload)
                    .then(response => {
                        console.log(response.data)
                        this.$buefy.toast.open({
                            message: 'Request submitted successfully',
                            type: 'is-success'
                        })
                        this.$emit('newRequestGenerated')
                        this.$parent.close()
                    })
                    .catch(function (error) {
                        var error_msg = "Request error"
                        if (error.response.data.detail != null){
                            error_msg = error.response.data.detail
                        }
                        current.$buefy.toast.open({
                            message: error_msg,
                            type: 'is-danger'
                        })
                    })
                }
                else {
                    console.log(payload)
                    client.put(`api/v1/staging/employee`, payload)
                    .then(response => {
                        console.log(response.data)
                        this.$buefy.toast.open({
                            message: 'Request submitted successfully',
                            type: 'is-success'
                        })
                        this.$emit('newRequestGenerated')
                        this.$parent.close()
                    })
                    .catch(function (error) {
                        var error_msg = "Request error"
                        if (error.response.data.detail != null){
                            error_msg = error.response.data.detail
                        }
                        current.$buefy.toast.open({
                            message: error_msg,
                            type: 'is-danger'
                        })
                    })
                }
            }
        }
    }
</script>