<template>
    <div class="columns">
        <div class="column is-8 is-offset-2">
            <GPNameTitle v-bind:practice_name="practice_name"/>
            <b-tabs v-model="activeTab" :animated=false>
                <b-tab-item label="GP Details">
                    <GPDetailsGeneralForm v-bind:practice_details="practice_details"
                                          @newRequestGenerated="newRequestGenerated"
                                          style="margin-bottom: 15px"/>
                    <GPDetailsAddressesForm v-bind:practice_details="practice_details"/>
                </b-tab-item>

                <b-tab-item label="Employees">
                    <GPEmployeesList v-bind:practice_id="practice_id"/>
                </b-tab-item>
            </b-tabs>
        </div>
    </div>
</template>

<script>
    import GPNameTitle from './general/GPNameTitle.vue'
    import GPDetailsGeneralForm from './DetailsGeneralForm.vue'
    import GPDetailsAddressesForm from './DetailsAddressesForm.vue'
    import GPEmployeesList from './EmployeesList.vue'
    import {getPracticeDetailsByName} from '../api.js'

    export default {
        name: 'PracticeForm',
        props: ['practice_name'],
        components: {
            GPNameTitle,
            GPDetailsGeneralForm,
            GPDetailsAddressesForm,
            GPEmployeesList
        },
        data() {
            return {
                activeTab: 0,
                practice_details: {},
                practice_id: 0
            }
        },
        async created() {
            this.practice_details = await getPracticeDetailsByName(this.$props.practice_name)
            this.practice_id = this.practice_details["id"]
        },
        methods: {
            newRequestGenerated() {
                this.$emit('newRequestGenerated')
            }
        }
    }
</script>

<style scoped>

    .layout {
        /* margin-left: 200px; */
        /* margin-right: 200px; */
        max-width: 1920px;
        /* position: absolute; */
        margin: auto;
        left: 0;
        right: 0;
        top: 5%;
        bottom: 0;
    }

</style>