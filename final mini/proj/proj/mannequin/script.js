// Get all interactive elements
const sizeButtons = document.querySelectorAll(".size-btn");
const skinButtons = document.querySelectorAll(".skin-btn");
const modelViewer = document.getElementById("model-viewer");
const visualizeBtn = document.querySelector(".visualize-button");

let selectedSize = null;
let selectedSkin = null;

// Set default model path (fallback)
const defaultModel = "models/BaseMashFemale.glb";
modelViewer.setAttribute("src", defaultModel);

// Size selection logic
sizeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    sizeButtons.forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");

    selectedSize = button.getAttribute("data-size");
    updateModelIfReady();
  });
});

// Skin selection logic (based on color buttons)
skinButtons.forEach((button) => {
  button.addEventListener("click", () => {
    skinButtons.forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");

    selectedSkin = button.getAttribute("data-skin");
    updateModelIfReady();
  });
});

// Visualize button click
// visualizeBtn.addEventListener("click", () => {
//   if (!selectedSize || !selectedSkin) {
//     alert("Please select both a size and a skin color.");
//   } else {
//     alert(`Showing model for Size: ${selectedSize}, Skin: ${selectedSkin}`);
//   }
// });

// Load 3D model dynamically based on selection
function updateModelIfReady() {
  if (selectedSize && selectedSkin) {
    const modelPath = `models/${selectedSize}/female_${selectedSize}_${selectedSkin}.glb`;

    console.log("🔄 Loading model from:", modelPath);
    modelViewer.setAttribute("src", modelPath);

    // Optional load/error listeners
    modelViewer.addEventListener("load", () => {
      console.log("✅ Model loaded successfully!");
    });

    modelViewer.addEventListener("error", () => {
      console.error("❌ Failed to load model at:", modelPath);
    });
  } else {
    // Fallback to default model if incomplete
    modelViewer.setAttribute("src", defaultModel);
  }
}


visualizeBtn.addEventListener("click", () => {
  if (!selectedSize || !selectedSkin) {
    alert("Please select both a size and a skin color.");
  } else {
    // Create the folder name like "S3" from skin selection
    const folderName = `${selectedSize}${selectedSkin}`;

    // Construct the relative path (make sure your server serves from project root)
    const redirectPath = `models/${selectedSize}tryon/${folderName}/index.html`;

    // /mannequin/mannequin/models/Stryon/S1/index.html
    // Optional: Log the path for debug
    console.log("➡️ Redirecting to:", redirectPath);

    // Redirect
    window.location.href = redirectPath;
  }
});


