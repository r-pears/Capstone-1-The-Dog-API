async function fetchRandomDog() {
  let result = document.querySelector('#result-section');
  let response = await axios.get(`https://api.thedogapi.com/v1/breeds`);
  let random = Math.floor(Math.random() * response.data.length);
  let randomDog = response.data.splice(random, 1)[0];

  result.innerHTML = '';

  let newPara = document.createElement('p');
  let newDog = document.createElement('a');
    newDog.innerHTML = `Read more about ` + randomDog.name + ` here.`;
    newDog.setAttribute('href', `/breed/${randomDog.name}`);
  const newImage = document.createElement('img');
    newImage.setAttribute('src', randomDog.image.url);
    newImage.classList.add('dog-image');

  newPara.appendChild(newDog);
  newPara.appendChild(newImage);
  result.appendChild(newPara);
}