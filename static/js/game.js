// script.js
const imageContainer = document.getElementById("image-container");
const scoreElement = document.getElementById("score");
let score = 0;
let flippedCards = [];

// Daftar path gambar yang sudah diacak
// Menggunakan perulangan for
const imagePaths = [];
for (let i = 0; i < 14; i++) {
    imagePaths.push(`static/img/img_${i}.jpg`);
}

// Duplicate daftar path gambar untuk membuat pasangan
const allImagePaths = [...imagePaths, ...imagePaths];

// Acak daftar path gambar
const shuffledImagePaths = shuffleArray(allImagePaths);

// Tambahkan kartu-kartu ke dalam elemen container
shuffledImagePaths.forEach((path, index) => {
    const card = document.createElement("div");
    card.className = "card";
    card.setAttribute("data-index", index);

    const inner = document.createElement("div");
    inner.className = "inner";

    const img = document.createElement("img");
    img.src = path;
    img.alt = "Image";
    img.className = "image";

    const cardBack = document.createElement("div");
    cardBack.className = "card-back";
    
    inner.appendChild(img);
    inner.appendChild(cardBack);

    card.appendChild(inner);

    card.addEventListener("click", revealCard);

    imageContainer.appendChild(card);
});

// Fungsi untuk mengacak array
function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// Fungsi untuk memunculkan kartu saat diklik
function revealCard(event) {
    const card = event.currentTarget;
    const index = card.getAttribute("data-index");

    // Cek apakah kartu sudah terbuka atau tidak
    if (card.classList.contains("opened")) {
        return;
    }

    card.querySelector(".card-back").style.display = "none";

    // Tambahkan kartu ke dalam daftar kartu yang telah terbuka
    flippedCards.push({ card, index });

    if (flippedCards.length === 2) {
        // Jika ada 2 kartu yang terbuka, cek apakah pasangan atau tidak
        const [firstCard, secondCard] = flippedCards;

        if (firstCard.card.querySelector(".image").src === secondCard.card.querySelector(".image").src) {
            // Kartu pasangan cocok
            setTimeout(() => {
                firstCard.card.classList.add("opened");
                secondCard.card.classList.add("opened");
                score += 1;
                scoreElement.innerText = `Score: ${score}`;
                flippedCards = [];
            }, 1000);
        } else {
            // Kartu pasangan tidak cocok
            setTimeout(() => {
                firstCard.card.querySelector(".card-back").style.display = "block";
                secondCard.card.querySelector(".card-back").style.display = "block";
                flippedCards = [];
            }, 1000);
        }
    }
}
