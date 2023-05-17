<template>
  <div class="modal-container" v-if="show">
    <div class="modal-background" @click="close"></div>
    <div class="modal-content" :style="{ backgroundColor: color }">
      <div class="modal-header">
        <img :src="album.cover" class="modal-cover" />
        <h3 class="modal-title" :style="{ color: text_color }">{{ album.title }}</h3>
        <p class="modal-artist" :style="{ color: text_color }">{{ album.artist }}</p>
      </div>
      <div class="modal-body">
        <ul class="modal-songs" :class="{ modalStory: chapters.length > 0 }">
          <li v-for="(song, index) in album.songs" :key="index">
            <div>
                {{ song }}
                <div class="chapter">{{ chapters[index] }}</div>
            </div></li>
        </ul>
      </div>
      <div class="modal-footer">
        <button class="modal-close" @click="close">Close</button>
        <button class="modal-generate" @click="generate">Generate</button>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "AlbumModal",
    data() {
        return {
            album: {},
            show: false,
            color: '',
            text_color: '',
            streamedData: [],
            isStreaming: false,
            chapters: []
        }
    },
    methods: {
      close() {
        this.emitter.emit("show-modal", false);
        this.show = false;
      },
      generate() {
        const api_url = 'http://localhost:5001/generate_album';
          const query_params = { album_id: this.album.album_id };
          this.isStreaming = true;
          this.chapters = [];
          fetch(api_url + '?' + new URLSearchParams(query_params), {mode: 'cors'})
              .then(response => {
              const reader = response.body.getReader();
              const decoder = new TextDecoder();
            
              const read = () => {
                return reader.read().then(({value, done}) => {
                  if (done) {
                    this.isStreaming=false;
                    return;
                  }

                  const chunk = decoder.decode(value, {stream: true});
                  this.streamedData.push(chunk);
                  console.log(chunk);
                  this.chapters.push(chunk)

                  return read();
                });
              };
              return read();
            })
              .then(data => {
                  console.log(data);

              })
              .catch(error => {
                  console.error('Error searching API:', error);
              });
      },
      getProminentColor(imageUrl, callback) {
        const img = new Image();
        img.crossOrigin = 'Anonymous';
        img.onload = function () {
            const canvas = document.createElement('canvas');
            canvas.width = this.width;
            canvas.height = this.height;

            const ctx = canvas.getContext('2d', {willReadFrequently: true});
            ctx.drawImage(this, 0, 0);

            const sampleSize = 4;
            let r = 0;
            let g = 0;
            let b = 0;

            for (let i = 0; i < sampleSize; i++) {
                const x = Math.floor(Math.random() * this.width);
                const y = Math.floor(Math.random() * this.height);
                const pixel = ctx.getImageData(x, y, 1, 1).data;
                r += pixel[0];
                g += pixel[1];
                b += pixel[2];
            }

            r = Math.floor(r / sampleSize);
            g = Math.floor(g / sampleSize);
            b = Math.floor(b / sampleSize);

            const color = `rgb(${r},${g},${b})`;
            callback(color);
        };
        img.src = imageUrl;
    },
    getTextColor(backgroundColor) {
        // Convert the hex color to an RGB triplet
        var color = backgroundColor.substring(4);
        color = color.split(',');
        color[2] = color[2].slice(0, -1)
        const r = parseInt(color[0]);
        const g = parseInt(color[1]);
        const b = parseInt(color[2]);

        // Calculate the relative luminance of the color
        const luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;

        // Choose black or white text based on the luminance
        if (luminance > 0.5) {
            return '#000000'; // black
        } else {
            return '#ffffff'; // white
        }
      }
    },
    mounted() {
        this.emitter.on("show-album", (msg) => {
            this.album = msg;
            this.chapters = [];
            this.getProminentColor(msg.cover, (nc) => {
                this.color = nc;
                this.text_color = this.getTextColor(this.color);
            });
        }),
        this.emitter.on("show-playlist", (msg) => {
            this.album = msg;
        }),
        this.emitter.on("show-modal", (msg) => {
            this.show = msg;
        })
    },
  };
</script>

<style>
.modal-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.modal-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: #fff;
  width: 500px;
  padding: 20px;
  border-radius: 10px;
  z-index: 20;
}

.modal-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.modal-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-top: 10px;
  margin-bottom: -6px;
}

.modal-artist {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.modal-cover {
  width: 200px;
  height: 200px;
  margin: 10px 0;
}

.modal-songs {
  list-style-type: none;
  padding: 10px;
  margin: 10px auto;
  max-height: 300px;
  overflow-y: auto;
  background-color: lightgrey;
  border-radius: 1em;
  width: 50%;
}

.modalStory {
  width: 80%;
}

.modal-songs li {
  font-size: 16px;
  color: #333;
  padding: 0.25em 0;
  padding: 0.5em 1em;
  padding-bottom: 0em;
  margin-bottom: -3px;
  border: darkgrey 3px solid;
}

.modal-close {
  background-color: #f44336;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
}

.modal-generate {
  background-color: #1dba01;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
  float: right;
}

.chapter {
  padding: 0.5em;
}

</style>
