<template>
    <div class="card">
        <div class="card-header-title">
            <p class="title is-3">
                General
            </p>
        </div>
        <div class="card-content">
            <section style="padding-right: 50px">
                <b-field label="Name" horizontal>
                    <b-input v-model="name" size="is-default"
                    placeholder="Enter a GP Practice Name"></b-input>
                </b-field>
                <b-field label="National Code" horizontal>
                    <b-input v-model="national_code" size="is-default" 
                    placeholder="Enter a National Code"></b-input>
                </b-field>
                <b-field label="EMIS CDB Practice Code" horizontal>
                    <b-input v-model="emis_cdb_practice_code" size="is-default" 
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
                <div class="level">
                    <div class="level-left field" horizontal>
                        <b-checkbox v-model="closed"
                            type="is-primary">
                                Practice closed
                        </b-checkbox>
                    </div>
                    <div class="level-right" style="padding-top: 20px">
                        <b-button type="is-primary" outlined>Save</b-button>
                    </div>
                </div>
            </section>
        </div>
    </div>
</template>

<script>

export default {
    name: 'GPDetailsGeneralForm',
    props: ['practice_details'],
    data() {
        const today = new Date()
        return {
            go_live_date: new Date(),
            minDate: new Date(today.getFullYear(), today.getMonth(), today.getDate()),
            name: '',
            national_code: '',
            emis_cdb_practice_code: '',
            closed: false,
        }
    },
    watch: { 
          practice_details: function(details) {
            this.name = details['name']
            this.national_code = details['national_code']
            this.emis_cdb_practice_code = details['emis_cdb_practice_code']
            this.go_live_date = new Date(details['go_live_date'])
            this.closed = details['closed']
        }
    },
    created() {
    }
}
</script>

<style scoped>
.title {
    font-weight: lighter;
}
</style>