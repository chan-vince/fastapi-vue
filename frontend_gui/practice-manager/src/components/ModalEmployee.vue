<template>
    <div class="modal-card" style="margin: 0px 50px 0px 50px">
        <header class="modal-card-head">
            <p class="modal-card-title">{{action}} Employee</p>
        </header>
        <section class="modal-card-body">
            <b-field label="Name" horizontal>
                <b-input
                    :value="rowObject.name"
                    v-model="name"
                    placeholder="Name(s)"
                    required>
                </b-input>
            </b-field>

            <b-field label="Email" horizontal>
                <b-input
                    :value="rowObject.email"
                    v-model="email"
                    placeholder="Email"
                    required>
                </b-input>
            </b-field>

            <b-field label="Job Title" horizontal>
                <b-select :placeholder="rowObject.job_title.title"
                v-model="title_id">
                    <option
                        v-for="title in job_titles"
                        :value="title.id"
                        :key="title.id">
                        {{ title.title }}
                    </option>
                </b-select>
            </b-field>

            <b-field label="Professional ID" horizontal>
                <b-input
                    :value="rowObject.professional_num"
                    v-model="professional_num"
                    placeholder="Professional ID"
                    required>
                </b-input>
            </b-field>

            <b-field label="IT Portal ID" horizontal>
                <b-input
                    :value="rowObject.it_portal_num"
                    v-model="it_portal_num"
                    placeholder="IT Portal ID">
                </b-input>
            </b-field>
            <b-field label="Desktop ID" horizontal>
                <b-input
                    :value="rowObject.desktop_num"
                    v-model="desktop_num"
                    placeholder="Desktop ID">
                </b-input>
            </b-field>

            <b-field label="Active" horizontal>
                <b-switch :value="rowObject.active"
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
                name: '',
                email: '',
                title_id: null,
                professional_num: null,
                it_portal_num: null,
                desktop_num: null,
                active: true,
                source_id: null
            }
        },
        created () {
            if (this.$props.jobTitles == null) {
                client.get(`api/v1/job_titles`)
                .then(response => {
                    this.job_titles = response.data
                })
            }
            else{
                this.job_titles = this.$props.jobTitles
            }
            if (this.rowObject != null){
                this.name = this.rowObject.name,
                this.email = this.rowObject.email,
                this.title_id = this.rowObject.job_title.id,
                this.professional_num = this.rowObject.professional_num,
                this.it_portal_num = this.rowObject.it_portal_num,
                this.desktop_num = this.rowObject.desktop_num,
                this.active = this.rowObject.active
                this.source_id = this.rowObject.id
            }
        },
        methods: {
            saveDetails() {
                var current = this;
                var payload = {
                    "name": this.name,
                    "email": this.email,
                    "job_title_id": this.title_id,
                    "professional_num": this.professional_num,
                    "it_portal_num": this.it_portal_num,
                    "desktop_num": this.desktop_num,
                    "active": this.active,
                    "source_id": this.source_id,
                    "requestor_id": 5000
                }
                console.log(payload)
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
                    console.log(error);
                    current.$buefy.toast.open({
                        message: 'Request error',
                        type: 'is-danger'
                    })
                })
            }
        }
    }
</script>