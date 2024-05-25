from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode


def record(path):
    js = Javascript('''
    async function record() {
      let rec;
      let chanks;
      const mineType = 'audio/wav';

      const div = document.createElement('div');
      const startRecord = document.createElement('button');
      startRecord.textContent = 'Rec';
      div.appendChild(startRecord);

      const stopRecord = document.createElement('button');
      stopRecord.textContent = 'Stop';
      stopRecord.style.display = 'none'
      div.appendChild(stopRecord);

      const audio = document.createElement('audio');
      div.appendChild(audio);

      document.body.appendChild(div);

      function handlerFunction(stream, resolve) {
          rec = new MediaRecorder(stream, {
              mimeType: mineType,
              audioBitsPerSecond: 706000,
              sampleRate: 44100
          });
          rec.ondataavailable = e => {
              chanks.push(e.data);
              if (rec.state == "inactive") {
                  let blob = new Blob(chanks, { type: mineType });
                  audio.src = URL.createObjectURL(blob);
                  audio.controls = true;
                  audio.autoplay = true;
                  resolve();
              }
          }
      }

      startRecord.onclick = e => {
          startRecord.style.display = 'none'
          stopRecord.style.display = 'block'
          chanks = [];
          rec.start();
      }

      stopRecord.onclick = e => {
        startRecord.style.display = 'block'
        stopRecord.style.display = 'none'
        rec.stop();
      }

      function blobToBase64(blob) {
        return new Promise((resolve, _) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result);
          reader.readAsDataURL(blob);
        });
      }

      await new Promise((resolve) => {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => { handlerFunction(stream, resolve) })
      });
      let blob = new Blob(chanks, { type: 'audio/mpeg-3' });
      return await blobToBase64(blob);
    }
    ''')

    display(js)
    data = eval_js('record()')
    binary = b64decode(data.split(',')[1])
    with open(path, 'wb') as f:
        f.write(binary)
    return path
