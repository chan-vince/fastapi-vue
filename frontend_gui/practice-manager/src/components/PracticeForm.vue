<template>
    <div class="columns">
        <div class="column is-three-fifths is-offset-one-fifth">
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
    import GPNameTitle from '../components/GPNameTitle.vue'
    import GPDetailsGeneralForm from '../components/GPDetailsGeneralForm.vue'
    import GPDetailsAddressesForm from '../components/GPDetailsAddressesForm.vue'
    import GPEmployeesList from '../components/GPEmployeesList.vue'
    import {client} from '../api.js'

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
        created() {
            this.getPracticeDetails()
        },
        methods: {
            getPracticeDetails(){
                client.get(`api/v1/practice/name`, {params: {name: this.$props.practice_name} })
                .then(response => {
                    this.practice_details = response.data
                    this.practice_id = response.data["id"]
                })
            },
            newRequestGenerated(){
                this.$emit('newRequestGenerated')
            }
        }
    }
</script>

<style scoped>

.layout {
    /* margin-left: 200px; */
    /* margin-right: 200px; */
    max-width: 1280px;
    position: absolute;
    margin: auto;
    left: 0;
    right: 0;
    top: 5%;
    bottom: 0;
}

</style>