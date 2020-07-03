<template>
    <div class="columns">
        <div class="column">
            <h1 class="pageTitle">{{pageTitle}}</h1>
        </div>
        <div class="column">
            <b-input
            autofocus
            v-model="searchInput"
            v-on:input="updateSearchInput"
            placeholder="Search by name..."
            icon="magnify"
            size="is-large"/>
        </div>
    </div>
</template>


<script>
    export default { 
        name: 'PracticesTable',
        props: ['pageTitle', 'minSearchLength'],
        data() {
            return {
                searchInput: ""
            }
        },
        methods: {
            updateSearchInput(){
                if (this.searchInput.length > this.minSearchLength){
                    this.$emit('newSearchInput', this.searchInput)
                }
                else {
                    this.$emit('newSearchInput', "")
                }
            }
        }
    }
</script>


<style scoped>
    h1.pageTitle {
        font-weight: bold;
        font-size: 30pt;
        text-align: left;
        /* margin-top: 10px; */
        /* padding-left: 0px; */
    }
    .columns {
        padding-top: 20px
    }
</style>
