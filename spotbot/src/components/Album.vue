<template>
    <div class="album-item">
      <div class="album-cover">
        <img :src="album.imageUrl" alt="Album Cover">
      </div>
      <div class="album-details">
        <div class="album-name">{{ album.name }}</div>
        <div class="artist-name">{{ album.artist }}</div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AlbumItem',
    props: {
      album: Object // assumes an object with the properties `name`, `artist`, and `imageUrl`
    }
  }
  </script>
  
  <style scoped>
  .album-item {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    background-color: white;
  }
  
  .album-cover {
    height: 6rem;
  }

  .album-cover img {
    width: 6rem;
    height: 6rem;
    margin-right: 1rem;
  }
  
  .album-details {
    display: flex;
    flex-direction: column;
  }
  
  .album-name {
    font-size: 1.25rem;
    font-weight: bold;
    text-align: start;
  }
  
  .artist-name {
    font-size: 1rem;
    color: #333;
    text-align: start;
  }
  </style>