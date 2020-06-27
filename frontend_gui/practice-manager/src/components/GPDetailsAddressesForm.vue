<template>
    <div class="card">
        <div class="card-header-title">
            <p class="title is-3">
                Branches
            </p>
        </div>
        <div class="card-content">
            <div class="card" v-for="(address, index) in addresses" :key="address.id">
                <div class="card-header-title">
                    <p class="title is-4">
                        Address {{ index + 1 }}
                    </p>
                </div>
                <div class="card-content" style="padding-right: 50px">
                    <b-field label="Line 1" horizontal>
                        <b-input v-model="address.line_1" size="is-default"
                            placeholder="Line 1 of Address"></b-input>
                    </b-field>
                    <b-field label="Line 2" horizontal>
                        <b-input v-model="address.line_2" size="is-default"
                            placeholder="Line 2 of Address"></b-input>
                    </b-field>
                    <b-field label="Town" horizontal>
                        <b-input v-model="address.town" size="is-default"
                            placeholder="Town"></b-input>
                    </b-field>
                    <b-field label="County" horizontal>
                        <b-input v-model="address.county" size="is-default"
                            placeholder="County"></b-input>
                    </b-field>
                    <b-field label="Postcode" horizontal>
                        <b-input v-model="address.postcode" size="is-default"
                            placeholder="Postcode"></b-input>
                    </b-field>
                    <b-field label="Contact email (DTS)" horizontal>
                        <b-input v-model="address.dts_email" size="is-default"
                            placeholder="Contact email"></b-input>
                    </b-field>
                    <div class="columns is-mobile">
                        <div class="column is-1 is-offset-11" style="padding-right: 0px">
                            <b-button type="is-primary" outlined>Save</b-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'GPDetailsAddressesForm',
    props: ['practice_details'],
    data() {
        const today = new Date()
        return {
            go_live_date: new Date(),
            minDate: new Date(today.getFullYear(), today.getMonth(), today.getDate()),
            addresses: []
        }
    },
    watch: { 
          practice_details: function(details) {
            this.addresses = details['addresses']
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