<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <SearchBar />
    <SearchResults />
  </div>
</template>

<script>
// @ is an alias to /src
import SearchBar from '@/components/SearchBar.vue'
import SearchResults from '@/components/SearchResults.vue'

export default {
  name: 'HomeView',
  components: {
    SearchBar,
    SearchResults
  }
}
</script>
