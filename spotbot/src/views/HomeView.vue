<template>
  <div class="home">
    <img class="logo" alt="Vue logo" src="../assets/logo.png">
    <SearchBar />
    <SearchResults />
    <album-modal />
  </div>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue'
import SearchResults from '@/components/SearchResults.vue'
import AlbumModal from '@/components/AlbumModal.vue'

export default {
  name: 'HomeView',
  components: {
    SearchBar,
    SearchResults,
    AlbumModal
  }
}
</script>

<style scoped>
.logo {
  width: 20rem;
  padding: 2rem;
  margin: auto;
  display: block;
}
</style>
