<template>
    <section class="layout">
        <GPNameTitle v-bind:practice_name="practice_name"/>
        <!-- <div class="block">
            <button class="button" @click="activeTab = 1">Set Music</button>
        </div>
        <div class="block">
            <b-switch v-model="showBooks"> Show Books item </b-switch>
        </div> -->
        <b-tabs v-model="activeTab" :animated=false>
            <b-tab-item label="GP Details">
                <GPDetailsGeneralForm v-bind:practice_details="practice_details"
                style="margin-bottom: 15px"/>
                <GPDetailsAddressesForm v-bind:practice_details="practice_details"/>
            </b-tab-item>

            <b-tab-item label="Employees">
                Lorem <br>
                ipsum <br>
                dolor <br>
                sit <br>
                amet.
            </b-tab-item>

            <b-tab-item label="Access Systems">
                What light is light, if Silvia be not seen? <br>
                What joy is joy, if Silvia be not by— <br>
                Unless it be to think that she is by <br>
                And feed upon the shadow of perfection? <br>
                Except I be by Silvia in the night, <br>
                There is no music in the nightingale.
            </b-tab-item>

            <b-tab-item label="IP Address Ranges">
                Nunc nec velit nec libero vestibulum eleifend.
                Curabitur pulvinar congue luctus.
                Nullam hendrerit iaculis augue vitae ornare.
                Maecenas vehicula pulvinar tellus, id sodales felis lobortis eget.
            </b-tab-item>
        </b-tabs>
    </section>
</template>

<script>
    import GPNameTitle from '../components/GPNameTitle.vue'
    import GPDetailsGeneralForm from '../components/GPDetailsGeneralForm.vue'
    import GPDetailsAddressesForm from '../components/GPDetailsAddressesForm.vue'
    import {client} from '../api.js'

    export default {
        name: 'PracticeForm',
        props: ['practice_name'],
        components: {
            GPNameTitle,
            GPDetailsGeneralForm,
            GPDetailsAddressesForm
        },
        data() {
            return {
                activeTab: 0,
                practice_details: {},
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
                })
            },
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