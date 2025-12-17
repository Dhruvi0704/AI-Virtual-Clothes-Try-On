const centerModel = document.getElementById("center-model");
const leftModel = document.getElementById("left-model");
const rightModel = document.getElementById("right-model");

const models = [
  "models/model1.glb",
  "models/model2.glb",
  "models/model3.glb",
  "models/model4.glb",
  "models/model5.glb",
  "models/model6.glb",
  "models/model7.glb",
  "models/model8.glb",
  "models/model9.glb",
  "models/model10.glb",
];

let currentIndex = 0;

function updateModels() {
  const leftIndex = (currentIndex - 1 + models.length) % models.length;
  const rightIndex = (currentIndex + 1) % models.length;

  leftModel.src = models[leftIndex];
  centerModel.src = models[currentIndex];
  rightModel.src = models[rightIndex];
}

document.getElementById("next").addEventListener("click", () => {
  currentIndex = (currentIndex + 1) % models.length;
  updateModels();
});

document.getElementById("prev").addEventListener("click", () => {
  currentIndex = (currentIndex - 1 + models.length) % models.length;
  updateModels();
});

updateModels(); // Initial load
