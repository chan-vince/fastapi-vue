<template>
    <section>
        <h1> {{ practice_name }}</h1>
    </section>
</template>

<script>
    export default {
        name: 'GPNameTitle',
        props: ['practice_name'],
        data() {
            return {
            }
        },
    }
</script>

<style scoped>
h1 {
    font-weight: bold;
    font-size: 30pt;
    text-align: left;
    margin-top: 60px;
    margin-bottom: 20px;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
}

</style>