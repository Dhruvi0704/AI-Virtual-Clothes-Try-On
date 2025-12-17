const products = [
  {
    name: "Tokyo Talkies",
    model: "dress1.glb",
    img: "dress1.png",
    desc: "Sheath Mini Dress",
    price: "₹239",
    original: "₹1999",
    discount: "88%",
    rating: "4.4 ★ | 5",
  },
  {
    name: "Tokyo Talkies",
    model: "dress2.glb",
    img: "dress2.png",
    desc: "Puff Sleeves Fit & Flare",
    price: "₹496",
    original: "₹3549",
    discount: "86%",
    rating: "3.6 ★ | 7",
  },
  {
    name: "Tokyo Talkies",
    model: "dress3.glb",
    img: "dress3.png",
    desc: "Classic White Dress",
    price: "₹2299",
    original: "₹3499",
    discount: "34%",
    rating: "4.1 ★ | 10",
  },
  {
    name: "Tokyo Talkies",
    model: "dress4.glb",
    img: "dress4.png",
    desc: "Trendy Floral Dress",
    price: "₹899",
    original: "₹1999",
    discount: "55%",
    rating: "4.8 ★ | 22",
  },
  {
    name: "Tokyo Talkies",
    model: "dress5.glb",
    img: "dress5.png",
    desc: "Black Elegance Gown",
    price: "₹1799",
    original: "₹2599",
    discount: "31%",
    rating: "4.5 ★ | 15",
  },
  {
    name: "Tokyo Talkies",
    model: "dress6.glb",
    img: "dress6.png",
    desc: "Traditional Saree Style",
    price: "₹3499",
    original: "₹4999",
    discount: "30%",
    rating: "4.2 ★ | 8",
  },
  {
    name: "Tokyo Talkies",
    model: "dress7.glb",
    img: "dress7.png",
    desc: "Pink Skater Dress",
    price: "₹1799",
    original: "₹2399",
    discount: "25%",
    rating: "4.0 ★ | 12",
  },
  {
    name: "Tokyo Talkies",
    model: "dress8.glb",
    img: "dress8.png",
    desc: "Denim Fusion",
    price: "₹2199",
    original: "₹2999",
    discount: "26%",
    rating: "4.3 ★ | 17",
  },
  {
    name: "Tokyo Talkies",
    model: "dress9.glb",
    img: "dress9.png",
    desc: "Embroidered Lehenga",
    price: "₹4599",
    original: "₹5999",
    discount: "23%",
    rating: "4.6 ★ | 9",
  },
  {
    name: "Tokyo Talkies",
    model: "dress10.glb",
    img: "dress10.png",
    desc: "Elegant Designer Dress",
    price: "₹3899",
    original: "₹4999",
    discount: "22%",
    rating: "4.7 ★ | 14",
  },
];

const grid = document.getElementById("productGrid");
const viewer = document.getElementById("modelViewer");

products.forEach((product) => {
  const card = document.createElement("div");
  card.className = "product-card";
  card.innerHTML = `
    <img src="images/${product.img}" alt="${product.name}">
    <div class="product-name">${product.name}</div>
    <div class="product-details">${product.desc}</div>
    <div class="price">${product.price}
      <span class="original-price">${product.original}</span>
      <span class="discount">(${product.discount} OFF)</span>
    </div>
    <div class="rating">${product.rating}</div>
  `;

  card.addEventListener("click", () => {
    const modelPath = `XL/${product.model}`;
    viewer.setAttribute("src", modelPath);
    console.log(`Model changed to: ${modelPath}`);
  });

  grid.appendChild(card);
});
