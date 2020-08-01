<template>
    <div class="modal-card">
        <header class="modal-card-head">
            <p class="modal-card-title">{{action}} Employee</p>
        </header>
        <section class="modal-card-body">
            <b-field label="Name" horizontal>
                <b-input :value="this.name" v-model="name" placeholder="Name(s)" required></b-input>
            </b-field>

            <b-field label="Email" horizontal>
                <b-input :value="this.email" v-model="email" placeholder="Email" required></b-input>
            </b-field>

            <b-field label="Job Title" horizontal>
                <b-select :placeholder="this.job_title.title" v-model="title_id" required>
                    <option v-for="title in job_titles" :value="title.id" :key="title.id">{{ title.title }}</option>
                </b-select>
            </b-field>

            <b-field label="Practice" horizontal>
                <b-autocomplete
                        v-model="practice_name"
                        :data="filteredPractices"
                        :placeholder="practice_name"
                        icon="magnify"
                        clearable
                        @select="option => selected = option"
                        required
                >
                    <template slot="empty">No results found</template>
                </b-autocomplete>
            </b-field>

            <b-field label="Professional ID" horizontal>
                <b-input
                        :value="this.professional_num"
                        v-model="professional_num"
                        placeholder="Professional ID"
                        required
                ></b-input>
            </b-field>

            <b-field label="IT Portal ID" horizontal>
                <b-input :value="this.it_portal_num" v-model="it_portal_num" placeholder="IT Portal ID"></b-input>
            </b-field>
            <b-field label="Desktop ID" horizontal>
                <b-input :value="this.desktop_num" v-model="desktop_num" placeholder="Desktop ID"></b-input>
            </b-field>

            <b-field label="Active" horizontal>
                <b-switch :value="this.active" v-model="active" type="is-success"></b-switch>
            </b-field>
        </section>
        <footer class="modal-card-foot">
            <button class="button is-primary" @click="saveDetails(rowObject)">Save</button>
            <button class="button" type="button" @click="$parent.close()">Cancel</button>
        </footer>
    </div>
</template>


<script>
import {getJobTitles, getPracticeDetailsByName, getPracticeNamesAll, postChangeRequest} from "@/api";

    export default {
        name: "ModalEmployee",
        props: ["rowObject", "jobTitles", "action"],
        components: {},
        data() {
            return {
                isComponentModalActive: false,
                job_titles: [],
                id: "",
                name: "",
                email: "",
                title_id: null,
                professional_num: null,
                it_portal_num: null,
                desktop_num: null,
                active: true,
                source_id: null,
                all_practices: [],
                practice_name: "",
                job_title: {title: ""}
            };
        },
        computed: {
            filteredPractices() {
                return this.all_practices.filter(option => {
                    return (
                        option
                            .toString()
                            .toLowerCase()
                            .indexOf(this.practice_name.toLowerCase()) >= 0
                    );
                });
            }
        },
        async created() {
            this.all_practices = await getPracticeNamesAll()
            if (this.$props.jobTitles == null) {
              this.job_titles = await getJobTitles()
            } else {
                this.job_titles = this.$props.jobTitles;
            }
            console.log(`Row object: ${this.rowObject}`);
            if (this.rowObject != null) {
                this.id = this.rowObject.id;
                this.name = this.rowObject.name;
                this.email = this.rowObject.email;
                this.title_id = this.rowObject.job_title.id;
                this.professional_num = this.rowObject.professional_num;
                this.it_portal_num = this.rowObject.it_portal_num;
                this.desktop_num = this.rowObject.desktop_num;
                this.active = this.rowObject.active;
                this.source_id = this.rowObject.id;
                this.practice_name = this.rowObject.practices[0].name || ""
            }
        },
        methods: {
            async saveDetails() {
                // Check if name is blank
                if (this.name.length === 0) {
                    this.$buefy.toast.open({
                        message: "Please select a practice",
                        type: "is-danger"
                    });
                    return
                }

                let payload = {
                    name: this.name,
                    email: this.email,
                    job_title_id: this.title_id,
                    professional_num: this.professional_num,
                    it_portal_num: this.it_portal_num,
                    desktop_num: this.desktop_num,
                    active: this.active
                };
                let body = {
                    requestor_id: 1,
                    target_name: "employee",
                    target_id: this.source_id,
                    new_state: payload
                };

                if (this.practice_name !== "") {
                  let practice = await getPracticeDetailsByName(this.practice_name)
                  payload.practice_ids = [practice.id]
                }

                try {
                  let response = await postChangeRequest(body);

                  console.log(response.data);
                  this.$buefy.toast.open({
                    message: "Request submitted successfully",
                    type: "is-success"
                  });
                  this.$parent.$emit("newRequestGenerated");
                  this.$parent.close();
                }
                catch (error) {
                  this.$buefy.toast.open({
                    message: "Request error",
                    type: "is-danger"
                  });
                }
            }
        }
    };
</script>