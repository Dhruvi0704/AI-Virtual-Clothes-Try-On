const modelViewer = document.getElementById("model-viewer");
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

document.getElementById("next").addEventListener("click", () => {
  currentIndex = (currentIndex + 1) % models.length;
  modelViewer.src = models[currentIndex];
});

document.getElementById("prev").addEventListener("click", () => {
  currentIndex = (currentIndex - 1 + models.length) % models.length;
  modelViewer.src = models[currentIndex];
});

document
  .querySelector(".visualize-button")
  .addEventListener("click", function () {
    window.location.href = "http://127.0.0.1:5500/proj/mannequin/index.html";
  });

