async function searchDog() {
  const getTitle = document.querySelector('#breed');
  const getDog = getTitle.innerHTML;

  const response = await axios.get(`https://api.thedogapi.com/v1/breeds/search?q=${getDog}`);
  const dogData = response.data[0];

  getDogImage(dogData.reference_image_id);
  addDogData(dogData);
};

async function getDogImage(image_id) {
  const image = document.querySelector('#image');
  const response = await axios.get(`https://api.thedogapi.com/v1/images/${image_id}`);

  const newImage = document.createElement('img');
  newImage.setAttribute('src', response.data.url);
  newImage.classList.add('dog-image')

  image.appendChild(newImage);
}

function addDogData(data) {
  const bred = document.querySelector('#bred-for');
  bred.innerHTML = `${data.name} was original bred for ${data.bred_for}.`;

  const group = document.querySelector('#breed-group');
  group.innerHTML = `${data.name} belongs to breed group ${data.breed_group}.`;

  const height_imperial = document.querySelector('#height-imperial');
  height_imperial.innerHTML = `${data.height.imperial} inches.`;

  const height_metric = document.querySelector('#height-metric');
  height_metric.innerHTML = `${data.height.metric} cm.`;

  const life_span = document.querySelector('#life-span');
  life_span.innerHTML = `${data.life_span} years.`;

  const weight_imperial = document.querySelector('#weight-imperial');
  weight_imperial.innerHTML = `${data.weight.imperial} pounds.`;

  const weight_metric = document.querySelector('#weight-metric');
  weight_metric.innerHTML = `${data.weight.metric} kilograms.`;

  const traits = document.querySelector('#traits');
  traits.innerHTML = `Typical traits for a ${data.name} are ${data.temperament}.`
}

searchDog();