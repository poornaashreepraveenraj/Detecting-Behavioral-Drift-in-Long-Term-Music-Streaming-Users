// ── STATE ──
const state = {
  genres: [],
  artists: [],
  time: 'morning',
  energy: 50,
  mood: 50,
  recommendations: []
};

// ── THEME LOGIC ──
function updateTheme(time) {
    document.documentElement.dataset.theme = time;
}
updateTheme('morning'); // Initial

// ── CURSOR ──
const cursor = document.getElementById('cursor');
const ring = document.getElementById('cursor-ring');
let mx = 0, my = 0, rx = 0, ry = 0;
document.addEventListener('mousemove', e => { 
    mx = e.clientX; my = e.clientY; 
    cursor.style.left = mx + 'px'; cursor.style.top = my + 'px'; 
});
function animRing() {
  rx += (mx - rx) * 0.12; ry += (my - ry) * 0.12;
  ring.style.left = rx + 'px'; ring.style.top = ry + 'px';
  requestAnimationFrame(animRing);
}
animRing();

function updateCursorInteractions() {
  document.querySelectorAll('a, button, .genre-pill, .time-card, input').forEach(el => {
    el.addEventListener('mouseenter', () => { 
        ring.style.width='60px'; ring.style.height='60px'; 
        cursor.style.transform='translate(-50%,-50%) scale(1.5)'; 
    });
    el.addEventListener('mouseleave', () => { 
        ring.style.width='40px'; ring.style.height='40px'; 
        cursor.style.transform='translate(-50%,-50%) scale(1)'; 
    });
  });
}

// ── PARTICLE BACKGROUND ──
const bgCanvas = document.getElementById('bg-canvas');
const bgCtx = bgCanvas.getContext('2d');
let W, H, particles = [];
function resize() { W = bgCanvas.width = innerWidth; H = bgCanvas.height = innerHeight; }
resize(); window.addEventListener('resize', resize);

class Particle {
  constructor() { this.reset(); }
  reset() {
    this.x = Math.random() * W; this.y = Math.random() * H;
    this.vx = (Math.random() - 0.5) * 0.3; this.vy = (Math.random() - 0.5) * 0.3;
    this.r = Math.random() * 2 + 0.5;
    this.life = 0; this.maxLife = Math.random() * 200 + 100;
  }
  update() { this.x += this.vx; this.y += this.vy; this.life++; if (this.life > this.maxLife) this.reset(); }
  draw() {
    bgCtx.beginPath(); bgCtx.arc(this.x, this.y, this.r, 0, Math.PI*2);
    bgCtx.fillStyle = window.getComputedStyle(document.documentElement).getPropertyValue('--cyan') + '44';
    bgCtx.fill();
  }
}
for (let i = 0; i < 80; i++) particles.push(new Particle());
function animBg() { bgCtx.clearRect(0,0,W,H); particles.forEach(p => { p.update(); p.draw(); }); requestAnimationFrame(animBg); }
animBg();

// ── INTERACTIONS ──
document.querySelectorAll('.genre-pill').forEach(pill => {
  pill.addEventListener('click', () => {
    const genre = pill.dataset.genre;
    if (state.genres.includes(genre)) {
      state.genres = state.genres.filter(g => g !== genre);
      pill.classList.remove('active');
    } else {
      state.genres.push(genre);
      pill.classList.add('active');
    }
  });
});

document.querySelectorAll('.time-card').forEach(card => {
  card.addEventListener('click', () => {
    document.querySelectorAll('.time-card').forEach(c => c.classList.remove('active'));
    card.classList.add('active');
    state.time = card.dataset.time;
    updateTheme(state.time);
  });
});
// Trigger morning by default
document.querySelector('[data-time="morning"]').click();

document.getElementById('energy-slider').addEventListener('input', (e) => {
  state.energy = e.target.value;
  document.getElementById('energy-val').innerText = state.energy + '%';
});
document.getElementById('mood-slider').addEventListener('input', (e) => {
  state.mood = e.target.value;
  document.getElementById('mood-val').innerText = state.mood + '%';
});

// ── GENERATE RECOMMENDATIONS ──
const generateBtn = document.getElementById('generate-btn');
const recsGrid = document.getElementById('recs-grid');
const recsSection = document.getElementById('recommendations');

generateBtn.addEventListener('click', async () => {
  state.artists = document.getElementById('artist-input').value.split(',').map(s => s.trim()).filter(s => s);
  
  generateBtn.innerHTML = '<span>Scanning Dataset...</span>';
  generateBtn.disabled = true;

  try {
    const res = await fetch('http://localhost:8000/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        genres: state.genres,
        artists: state.artists,
        time_of_day: state.time,
        energy_preference: Number(state.energy),
        mood_preference: Number(state.mood)
      })
    });
    const data = await res.json();
    state.recommendations = data.recommendations;
    renderRecommendations();
  } catch (err) {
    console.error("Backend offline", err);
    alert("Please ensure the FastAPI backend is running on port 8000.");
  } finally {
    generateBtn.innerHTML = '<span>Analyze & Recommend</span>';
    generateBtn.disabled = false;
  }
});

function renderRecommendations() {
  recsSection.style.display = 'block';
  recsGrid.innerHTML = '';
  
  if (state.recommendations.length === 0) {
      recsGrid.innerHTML = '<p style="text-align:center; grid-column: 1/-1;">No high-accuracy matches found. Try adjusting your preferences.</p>';
      return;
  }

  state.recommendations.forEach((song, i) => {
    const card = document.createElement('div');
    card.className = 'song-card';
    card.style.transitionDelay = `${i * 80}ms`;
    
    // Platform icons Mapping
    const spotifyIcon = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg';
    const youtubeIcon = 'https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg';
    const appleIcon = 'https://upload.wikimedia.org/wikipedia/commons/2/2a/Apple_Music_logo.svg';
    const soundcloudIcon = 'https://upload.wikimedia.org/wikipedia/commons/a/a2/Antu_soundcloud.svg';

    card.innerHTML = `
      <div class="song-artwork-wrap">
        <div class="song-artwork" style="background: linear-gradient(135deg, var(--cyan), var(--violet)); display: flex; align-items: center; justify-content: center; font-size: 3rem; border-radius: 12px; aspect-ratio: 1;">🎵</div>
        <div class="song-links-overlay">
            <a href="${song.links.spotify}" target="_blank" class="platform-link"><img src="${spotifyIcon}"></a>
            <a href="${song.links.youtube}" target="_blank" class="platform-link"><img src="${youtubeIcon}"></a>
            <a href="${song.links.apple}" target="_blank" class="platform-link"><img src="${appleIcon}"></a>
            <a href="${song.links.soundcloud}" target="_blank" class="platform-link"><img src="${soundcloudIcon}"></a>
        </div>
      </div>
      <div class="song-title">${song.title}</div>
      <div class="song-artist">${song.artist}</div>
      <div class="song-meta">
        <span class="song-genre">${song.genre}</span>
        <span class="match-badge">${song.match_score}% Match</span>
      </div>
      <div class="energy-wrap">
        <div class="energy-fill" style="width: ${song.energy}%"></div>
      </div>
    `;
    recsGrid.appendChild(card);
    setTimeout(() => card.classList.add('show'), 50);
  });

  recsSection.scrollIntoView({ behavior: 'smooth' });
  drawRadarChart();
  updateCursorInteractions();
}

// ── VISUALIZATION ──
const fc = document.getElementById('featureCanvas');
const fx = fc.getContext('2d');
fc.width = 600; fc.height = 400;

function drawRadarChart() {
  if (state.recommendations.length === 0) return;
  
  fx.clearRect(0,0,600,400);
  const cx = 300, cy = 200, r = 140;
  const labels = ['Energy', 'Valence', 'Tempo', 'Danceability', 'Acousticness'];
  const n = labels.length;
  const angles = labels.map((_,i) => (i/n)*Math.PI*2 - Math.PI/2);
  
  // Average features from recommendations
  const avgE = state.recommendations.reduce((a,b) => a + b.energy, 0) / state.recommendations.length / 100;
  const avgV = state.recommendations.reduce((a,b) => a + b.valence, 0) / state.recommendations.length / 100;
  const avgT = state.recommendations.reduce((a,b) => a + b.tempo, 0) / state.recommendations.length / 220; // Bound tempo
  
  // Dummy data for others since we don't return all from backend for UI simplicity
  const vals = [avgE, avgV, avgT, (avgE+avgV)/2, 0.4];

  // Radar Grid
  fx.strokeStyle = window.getComputedStyle(document.documentElement).getPropertyValue('--border');
  for (let gr = 1; gr <= 4; gr++) {
    fx.beginPath();
    angles.forEach((a,i) => {
      const x = cx + Math.cos(a)*r*(gr/4);
      const y = cy + Math.sin(a)*r*(gr/4);
      i===0 ? fx.moveTo(x,y) : fx.lineTo(x,y);
    });
    fx.closePath();
    fx.stroke();
  }

  // Data Shape
  fx.beginPath();
  vals.forEach((v,i) => {
    const x = cx + Math.cos(angles[i])*r*v;
    const y = cy + Math.sin(angles[i])*r*v;
    i===0 ? fx.moveTo(x,y) : fx.lineTo(x,y);
  });
  fx.closePath();
  fx.fillStyle = window.getComputedStyle(document.documentElement).getPropertyValue('--cyan') + '33';
  fx.fill();
  fx.strokeStyle = window.getComputedStyle(document.documentElement).getPropertyValue('--cyan');
  fx.lineWidth = 1.5;
  fx.stroke();

  // Labels
  angles.forEach((a,i) => {
    const lx = cx + Math.cos(a)*(r+30);
    const ly = cy + Math.sin(a)*(r+30);
    fx.fillStyle = window.getComputedStyle(document.documentElement).getPropertyValue('--muted');
    fx.font = '10px Space Mono'; fx.textAlign='center';
    fx.fillText(labels[i], lx, ly);
  });
}

updateCursorInteractions();
window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    if (scrollY > 50) nav.style.padding = '0.8rem 4rem';
    else nav.style.padding = '1.2rem 4rem';
});
