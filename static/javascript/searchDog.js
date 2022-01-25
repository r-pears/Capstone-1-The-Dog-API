async function searchDog() {
  const getTitle = document.querySelector('#breed');
  const getDog = getTitle.innerHTML;

  const response = await axios.get(`https://api.thedogapi.com/v1/breeds/search?q=${getDog}`);
  const dogData = response.data[0];
  getDogImage(dogData.reference_image_id);

  console.log(dogData)
};

async function getDogImage(image_id) {
  const image = document.querySelector('#image');
  const response = await axios.get(`https://api.thedogapi.com/v1/images/${image_id}`);

  const newImage = document.createElement('img');
  newImage.setAttribute('src', response.data.url);

  image.appendChild(newImage);
}

searchDog();