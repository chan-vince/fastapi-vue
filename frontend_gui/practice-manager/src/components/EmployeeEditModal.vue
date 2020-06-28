<template>
    <div class="modal-card" style="margin: 0px 50px 0px 50px">
        <header class="modal-card-head">
            <p class="modal-card-title">{{action}} Employee</p>
        </header>
        <section class="modal-card-body">
            <b-field label="First Name" horizontal>
                <b-input
                    :value="rowObject.first_name"
                    placeholder="First Name"
                    required>
                </b-input>
            </b-field>

            <b-field label="Last Name" horizontal>
                <b-input
                    :value="rowObject.last_name"
                    placeholder="Last Name"
                    required>
                </b-input>
            </b-field>

            <b-field label="Email" horizontal>
                <b-input
                    :value="rowObject.email"
                    placeholder="Email"
                    required>
                </b-input>
            </b-field>

            <b-field label="Job Title" horizontal>
                <b-select :placeholder="rowObject.job_title.title">
                    <option
                        v-for="title in jobTitles"
                        :value="title.title"
                        :key="title.id">
                        {{ title.title }}
                    </option>
                </b-select>
            </b-field>

            <b-field label="Professional ID" horizontal>
                <b-input
                    :value="rowObject.professional_num"
                    placeholder="Professional ID"
                    required>
                </b-input>
            </b-field>

            <b-field label="IT Portal ID" horizontal>
                <b-input
                    :value="rowObject.it_portal_num"
                    placeholder="IT Portal ID">
                </b-input>
            </b-field>
            <b-field label="Desktop ID" horizontal>
                <b-input
                    :value="rowObject.desktop_num"
                    placeholder="Desktop ID">
                </b-input>
            </b-field>

            <b-field label="Active" horizontal>
                <b-switch :value="rowObject.active"
                type="is-success">
                </b-switch>
            </b-field>

        </section>
        <footer class="modal-card-foot">
            <button class="button" type="button" @click="$parent.close()">Cancel</button>
            <button class="button is-primary">Save</button>
        </footer>
    </div>
</template>


<script>
    export default {
        name: 'EmployeeEditModal',
        props: ["rowObject", "jobTitles", "action"],
        components: {
            
        },
        data() {
            return {
                isComponentModalActive: false,
            }
        },
        created () {
            // console.log(this.$props.jobTitles)
            // console.log(this.$props.rowObject)
        }
    }
</script>