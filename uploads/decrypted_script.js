const icons = ['🚀', '💻', '💡', '⚙️', '🌐', '📱', '🔒', '📊'];
let cardsArray = [];
let flippedCards = [];
let matchedPairs = 0;

let level = 1; 
let score = 0; 
let lives = 3; 
let moves = 0;
let timerInterval = null; 
let timeLeft = 60; 
let lockBoard = true; 

const grid = document.getElementById("grid"); 
let highScore = localStorage.getItem("highScore") || 0; 

function startGame() { 
    document.getElementById("gameOver").classList.add("hidden"); 
    document.getElementById("startBtn").classList.add("hidden");
    
    level = 1; 
    score = 0; 
    lives = 3; 
    
    startLevel();
}

function startLevel() {
    clearInterval(timerInterval);
    flippedCards = [];
    matchedPairs = 0;
    moves = 0;
    lockBoard = true; 
    
    timeLeft = Math.max(60 - ((level - 1) * 5), 20); 
    document.getElementById("timer").innerText = timeLeft; 
    
    updateUI();
    generateGrid();
    
    const allCards = document.querySelectorAll('.card');
    allCards.forEach(card => card.classList.add('flipped'));

    setTimeout(() => {
        allCards.forEach(card => card.classList.remove('flipped'));
        lockBoard = false; 
        startTimer(); 
    }, 5000);
}

function generateGrid() {
    grid.innerHTML = ""; 
    cardsArray = [...icons, ...icons];
    cardsArray.sort(() => 0.5 - Math.random());

    cardsArray.forEach((icon) => { 
        let card = document.createElement("div"); 
        card.classList.add("card"); 
        card.dataset.icon = icon; 
        
        card.innerHTML = `
            <div class="card-inner">
                <div class="card-front">❓</div>
                <div class="card-back">${icon}</div>
            </div>
        `;
        
        card.addEventListener("click", () => flipCard(card)); 
        grid.appendChild(card); 
    });
}

function flipCard(card) { 
    if (lockBoard || card.classList.contains("flipped")) return; 
    
    card.classList.add("flipped"); 
    flippedCards.push(card); 
    
    if (flippedCards.length === 2) { 
        moves++; // Increment move counter every time 2 cards are flipped
        checkMatch();
    }
}

function checkMatch() {
    lockBoard = true; 
    let [card1, card2] = flippedCards;
    
    if (card1.dataset.icon === card2.dataset.icon) {
        matchedPairs++;
        score += 10;
        updateUI();
        resetTurn();
        
        if (matchedPairs === icons.length) {
            clearInterval(timerInterval);
            triggerConfetti(); // CELEBRATE!
            
            // Add bonus score based on remaining time and lives
            score += (timeLeft * 2) + (lives * 10);
            
            level++;
            setTimeout(startLevel, 2500); // Give them time to see the confetti before next level
        }
    } else {
        lives--;
        updateUI();
        
        if (lives <= 0) {
            setTimeout(() => gameOver("Out of Lives!"), 600);
        } else {
            setTimeout(() => {
                card1.classList.remove("flipped");
                card2.classList.remove("flipped");
                resetTurn();
            }, 1000);
        }
    }
}

function resetTurn() {
    flippedCards = [];
    lockBoard = false;
}

function calculateStars() {
    // 8 perfect moves is 3 stars. 
    if (moves <= 10) return "⭐⭐⭐";
    if (moves <= 15) return "⭐⭐";
    if (moves <= 20) return "⭐";
    return "💔"; // Too many moves!
}

function startTimer() { 
    document.getElementById("timer").innerText = timeLeft; 
    
    timerInterval = setInterval(() => { 
        timeLeft--; 
        document.getElementById("timer").innerText = timeLeft; 
        
        if (timeLeft <= 0) {   
            clearInterval(timerInterval);
            gameOver("Time's Up!"); 
        }
    }, 1000); 
}

function updateUI() { 
    document.getElementById("score").innerText = score; 
    document.getElementById("level").innerText = level; 
    document.getElementById("lives").innerText = lives; 
    document.getElementById("moves").innerText = moves;
    document.getElementById("stars").innerText = calculateStars();
}

function triggerConfetti() {
    // Fire confetti from the left and right edges
    confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6, x: 0.2 }
    });
    confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6, x: 0.8 }
    });
}

function gameOver(message) { 
    clearInterval(timerInterval); 
    lockBoard = true; 
    
    document.getElementById("endMessage").innerText = message;
    document.getElementById("finalScore").innerText = score;
    document.getElementById("gameOver").classList.remove("hidden"); 

    if (score > highScore) { 
        highScore = score;
        localStorage.setItem("highScore", highScore); 
        triggerConfetti(); // Celebrate high score!
    }
    
    document.getElementById("highScore").innerText = highScore; 
}