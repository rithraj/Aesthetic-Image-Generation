async function loadModel() {
  model = await tf.loadLayersModel('https://storage.googleapis.com/diffusiondb-images/modelstuff/model.json', {requestInit:{mode:'cors', headers:{'Content-Type':'application/json'}}});
}

function tokenize(text) {
  text = text.toLowerCase();
  text = text.replace(/[!"#$%&()*+,-./:;<=>?@\[\\\]\^_`{|}~\t\n]/g, '')
  var split_text = text.split(' ');
  var tokens = [];
  split_text.forEach(element => {
      if (tokenizer_dictionary[element] != undefined) {
          tokens.push(tokenizer_dictionary[element]);
        }
  });
  var j = tokens.length
  while (j < 100) {
    tokens.push(0)
    j += 1
  }
  console.log(tokens.length)
  return tokens;
}

// get the score of the input text
function predict(text) {
  var x = tokenize(text)
  var y = model.predict(tf.tensor2d(x, [1, 100]));
  var score = y.dataSync()[0]
}