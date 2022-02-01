async function searchBreed() {
  let searchDog = document.querySelector('#search').value;
  let searchResult = document.querySelector('#search-result');
  let response = await axios.get(`https://api.thedogapi.com/v1/breeds`);
  let allDogsArray = response.data;
  searchResult.innerHTML = '';

  allDogsArray.forEach(dog => {
    if (dog.name.toLowerCase().startsWith(searchDog.toLowerCase())) {
      let newLi = document.createElement('li');

      let newDog = document.createElement('a');
      newDog.innerHTML = dog.name;
      newDog.setAttribute('href', `/breed/${dog.name}`)

      newLi.appendChild(newDog);
      searchResult.appendChild(newLi);
    }
  })
}