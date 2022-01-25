async function getAllDogs() {
  let response = await axios.get(`https://api.thedogapi.com/v1/breeds`);
  let allDogsArray = response.data;

  allDogsArray.forEach(dog => {
    console.log(dog.name)    
  });
}