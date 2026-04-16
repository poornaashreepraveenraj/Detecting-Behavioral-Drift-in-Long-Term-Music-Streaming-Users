import pandas as pd
import numpy as np
import random
import os

# Artist to Genre mapping for top artists
GENRE_MAP = {
    'Drake': 'Hip-Hop', 'Post Malone': 'Hip-Hop', 'Travis Scott': 'Hip-Hop', 'Kanye West': 'Hip-Hop',
    'The Weeknd': 'Pop', 'Taylor Swift': 'Pop', 'Ariana Grande': 'Pop', 'Justin Bieber': 'Pop',
    'Nirvana': 'Rock', 'Queen': 'Rock', 'Pink Floyd': 'Rock', 'The Beatles': 'Rock',
    'Miles Davis': 'Jazz', 'John Coltrane': 'Jazz', 'Dave Brubeck': 'Jazz',
    'deadmau5': 'Electronic', 'Daft Punk': 'Electronic', 'Avicii': 'Electronic',
    'Claude Debussy': 'Classical', 'Ludwig van Beethoven': 'Classical', 'Frédéric Chopin': 'Classical',
    'Sleepy Fish': 'Lo-fi', 'Idealism': 'Lo-fi', 'Jinsang': 'Lo-fi'
}

class AdvancedRecommender:
    def __init__(self):
        self.df = self._load_data()
        
    def _load_data(self):
        files = ['SpotifyAudioFeaturesApril2019.csv', 'SpotifyAudioFeaturesNov2018.csv']
        dfs = []
        for f in files:
            if os.path.exists(f):
                temp_df = pd.read_csv(f)
                dfs.append(temp_df)
        
        if not dfs:
            return pd.DataFrame()
            
        full_df = pd.concat(dfs).drop_duplicates(subset=['track_id'])
        full_df = full_df[['artist_name', 'track_name', 'energy', 'valence', 'tempo', 'danceability', 'acousticness', 'popularity']].dropna()
        
        # Normalize features
        full_df['energy_norm'] = full_df['energy']
        full_df['valence_norm'] = full_df['valence']
        full_df['tempo_norm'] = (full_df['tempo'] - full_df['tempo'].min()) / (full_df['tempo'].max() - full_df['tempo'].min())
        
        return full_df

    def get_recommendations(self, genres, artists, time_of_day, energy_pref, mood_pref):
        if self.df.empty:
            return []

        # Target Vector
        energy_target = energy_pref / 100.0
        mood_target = mood_pref / 100.0
        
        context_profiles = {
            'morning': {'energy': 0.4, 'valence': 0.6, 'tempo': 0.4},
            'afternoon': {'energy': 0.8, 'valence': 0.8, 'tempo': 0.7},
            'evening': {'energy': 0.6, 'valence': 0.5, 'tempo': 0.5},
            'night': {'energy': 0.3, 'valence': 0.3, 'tempo': 0.3}
        }
        profile = context_profiles.get(time_of_day, context_profiles['morning'])
        
        # Weighted Targets
        target_e = (energy_target * 0.7) + (profile['energy'] * 0.3)
        target_v = (mood_target * 0.7) + (profile['valence'] * 0.3)
        target_t = profile['tempo']

        subset = self.df.sort_values(by='popularity', ascending=False).head(20000).copy()
        
        # Euclidean distance for basic similarity (0 - 1 range)
        dist = np.sqrt(
            (subset['energy_norm'] - target_e)**2 +
            (subset['valence_norm'] - target_v)**2 +
            (subset['tempo_norm'] - target_t)**2
        )
        
        # Normalize distance to 0-100 score
        # Base Match Score (Max 70 points)
        subset['match_score'] = (1 - (dist / np.max(dist))) * 70
        
        # Artist Match Bonus (Weight: 20%)
        if artists and artists[0]:
            artists_lower = [a.lower().strip() for a in artists]
            subset.loc[subset['artist_name'].str.lower().isin(artists_lower), 'match_score'] += 20
            
        # Genre Influence (Weight: 10%)
        if genres:
            def match_genre(artist):
                g = GENRE_MAP.get(artist)
                return 1 if g in genres else 0
            subset['match_score'] += subset['artist_name'].apply(match_genre) * 10

        # Capping at 100% strictly
        subset['match_score'] = subset['match_score'].clip(upper=100.0)
        
        # --- DIVERSITY FILTERING ---
        # 1. Get top 50 matches first
        top_candidates = subset.sort_values(by='match_score', ascending=False).head(50)
        
        # 2. Limit to max 2 songs per artist
        diverse_results = []
        artist_count = {}
        
        for _, row in top_candidates.iterrows():
            artist = row['artist_name']
            if artist_count.get(artist, 0) < 2:
                diverse_results.append(row)
                artist_count[artist] = artist_count.get(artist, 0) + 1
            if len(diverse_results) >= 12:
                break
                
        # Final output formatting
        results = []
        for row in diverse_results:
            genre = GENRE_MAP.get(row['artist_name'], 'Alternative')
            results.append({
                "title": row['track_name'],
                "artist": row['artist_name'],
                "genre": genre,
                "energy": round(row['energy'] * 100),
                "valence": round(row['valence'] * 100),
                "tempo": round(row['tempo']),
                "match_score": round(row['match_score'], 1),
                "links": self._generate_links(row['track_name'], row['artist_name'])
            })
            
        return results

    def _generate_links(self, track, artist):
        q = f"{track} {artist}".replace(" ", "%20")
        return {
            "spotify": f"https://open.spotify.com/search/{q}",
            "apple": f"https://music.apple.com/us/search?term={q}",
            "youtube": f"https://www.youtube.com/results?search_query={q}",
            "soundcloud": f"https://soundcloud.com/search?q={q}"
        }

recommender = AdvancedRecommender()
