async function getAllDogs() {
  const dogList = document.querySelector('#allDogs');
  let response = await axios.get(`https://api.thedogapi.com/v1/breeds`);
  let allDogsArray = response.data;

  allDogsArray.forEach(dog => {
    let newLi = document.createElement('li');

    let newDog = document.createElement('a');
    newDog.innerHTML = dog.name;
    newDog.setAttribute('href', `/breed/${dog.name}`)

    newLi.appendChild(newDog);
    dogList.appendChild(newLi);
  });
}

getAllDogs();