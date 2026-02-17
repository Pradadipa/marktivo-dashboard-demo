# 📖 Data Dictionary — Module 2: Organic Architecture

> Dokumen ini menjelaskan seluruh kolom data yang digunakan di Module 2: Organic Architecture (The Brand Terminal).
> Platforms: Instagram, TikTok, YouTube, LinkedIn
> Data Sources: Platform Native APIs + Social Media Management Tools

---

## 1. `generate_organic_data()` — Cross-Platform Organic Metrics

Data harian per platform yang mencakup follower growth, engagement, reach, dan traffic metrics. Satu baris = satu hari × satu platform.

### Kolom Utama (Raw)

| Kolom | Tipe | Range (Dummy) | Penjelasan | Sumber di Production |
|-------|------|---------------|------------|---------------------|
| `date` | datetime | 30 hari terakhir | Tanggal data | — |
| `platform` | str | Instagram, TikTok, YouTube, LinkedIn | Nama platform social media | — |
| `followers` | int | 8,900 – 52,000+ | Total jumlah followers kumulatif pada hari itu. Naik terus tapi bisa turun kalau ada unfollow. | IG: Instagram Graph API `followers_count` · TT: TikTok API `follower_count` · YT: YouTube Data API `subscriberCount` · LI: LinkedIn API `followersCount` |
| `follower_growth` | int | -50 s/d +400 | Perubahan followers hari itu (bisa negatif kalau banyak unfollow). 15% chance negatif. | Dihitung: selisih `followers` hari ini vs kemarin |
| `impressions` | int | 3,000 – 96,000 | Jumlah kali konten tampil di feed/explore orang. Weekend di-boost +20%. | IG: `impressions` · TT: `video_views` (approximate) · YT: `impressions` · LI: `impressions` |
| `likes` | int | varies | Jumlah likes pada semua konten hari itu. Dihitung: `impressions × engagement_multiplier × random(0.6-1.4)`. | IG: `likes` · TT: `digg_count` · YT: `likes` · LI: `likes` |
| `comments` | int | 5-15% dari likes | Jumlah komentar. Rasio terhadap likes realistis untuk social media. | IG: `comments` · TT: `comment_count` · YT: `comments` · LI: `comments` |
| `shares` | int | 3-10% dari likes | Jumlah share/repost/retweet. Metrik penting untuk virality. | IG: `shares` · TT: `share_count` · YT: `shares` (via Data API) · LI: `shares` |
| `saves` | int | 8-20% dari likes | Jumlah save/bookmark. Indikator kuat bahwa konten bernilai tinggi bagi audience. | IG: `saved` · TT: `collect_count` · YT: N/A (gunakan `likes` sebagai proxy) · LI: N/A |
| `views` | int | 2,000 – 100,000 | Video views (untuk Reels, Shorts, TikTok). Berbeda dari impressions — views = orang benar-benar menonton. | IG: `video_views` · TT: `play_count` · YT: `viewCount` · LI: `views` |
| `profile_visits` | int | 2-6% dari impressions | Jumlah orang yang mengunjungi profil setelah melihat konten. | IG: `profile_views` · TT: `profile_views` · YT: channel page views · LI: `page_views` |
| `link_clicks` | int | 10-30% dari profile_visits | Jumlah klik pada link di bio/profil. Metrik traffic — orang yang benar-benar pindah ke website. | IG: `website_clicks` · TT: link click (limited) · YT: `card_clicks` · LI: `click_count` |
| `posts_published` | int | 0 atau 1 | Apakah ada konten yang dipost hari itu. Probabilitas berdasarkan target per minggu. | Internal tracking / scheduling tool (Later, Buffer, Hootsuite) |
| `posts_goal_weekly` | int | 2-5 per platform | Target jumlah posting per minggu. Dipakai untuk hitung Consistency Score. | Ditetapkan oleh content strategy / client agreement |

### Kolom Turunan (Calculated)

| Kolom | Tipe | Rumus | Benchmark | Penjelasan |
|-------|------|-------|-----------|------------|
| `engagement_rate` | float | (Likes + Comments + Shares) ÷ Impressions × 100 | > 5% | **Metric #1 untuk organic.** Mengukur seberapa banyak orang yang berinteraksi vs yang melihat. ER di bawah 5% = konten kurang resonan. |
| `share_of_voice` | float | (Saves + Shares) ÷ Impressions × 100 | > 2% | **The "Virality" Metric.** Saves dan shares adalah sinyal terkuat bahwa konten bernilai. Kalau orang save = mereka mau lihat lagi. Kalau share = mereka rekomendasikan ke orang lain. |
| `profile_conversion_rate` | float | Link Clicks ÷ Profile Visits × 100 | > 15% | **The "Traffic" Metric.** Dari orang yang cukup tertarik untuk lihat profil, berapa persen yang benar-benar klik link ke website. Kalau rendah = bio/profil kurang compelling atau link tidak relevan. |

---

## 2. `generate_content_library()` — Individual Post Data

Data per-post individual untuk Content Library dan Content Leaderboard. Satu baris = satu post.

### Kolom Utama

| Kolom | Tipe | Range (Dummy) | Penjelasan | Sumber di Production |
|-------|------|---------------|------------|---------------------|
| `post_id` | str | POST-001 s/d POST-048 | Unique identifier per post. | IG: `media_id` · TT: `video_id` · YT: `video_id` · LI: `activity_id` |
| `title` | str | 48 variasi judul | Judul/caption singkat dari post. | IG: `caption` (trimmed) · TT: `desc` · YT: `title` · LI: `commentary` |
| `platform` | str | Instagram, TikTok, YouTube, LinkedIn | Platform dimana post dipublish. | — |
| `content_type` | str | varies per platform | Format konten. Setiap platform punya tipe berbeda. | IG: `media_type` · TT: infer from metadata · YT: `videoType` · LI: `media_type` |
| `date` | str | 30 hari terakhir (YYYY-MM-DD) | Tanggal post dipublish. | IG: `timestamp` · TT: `createTime` · YT: `publishedAt` · LI: `created_at` |
| `views` | int | 500 – 150,000 | Total views/plays. Range lebar karena beberapa post bisa viral. | IG: `video_views` atau `impressions` · TT: `play_count` · YT: `viewCount` · LI: `views` |
| `likes` | int | 3-12% dari views | Jumlah likes pada post ini. | Per-post metric dari masing-masing platform API |
| `comments` | int | 5-20% dari likes | Jumlah komentar. | Per-post metric dari masing-masing platform API |
| `shares` | int | 2-15% dari likes | Jumlah share/repost. | Per-post metric dari masing-masing platform API |
| `saves` | int | 5-25% dari likes | Jumlah save/bookmark. | Per-post metric dari masing-masing platform API |
| `link_clicks` | int | 0.5-3% dari views | Jumlah klik link dari post ini. | IG: `website_clicks` (Story/Reel link sticker) · TT: limited · YT: `card_clicks` · LI: `click_count` |

### Kolom Turunan (Calculated)

| Kolom | Tipe | Rumus | Penjelasan |
|-------|------|-------|------------|
| `virality_score` | float | (Shares + Saves) ÷ Views × 100 | **Seberapa "shareable" post ini.** Score tinggi = orang mau menyebarkan ke orang lain. Dipakai untuk sorting di Content Library dan menentukan 🏆 Most Shared di Leaderboard. |
| `conversion_score` | float | Link Clicks ÷ Views × 100 | **Seberapa efektif post ini membawa traffic ke website.** Score tinggi = post ini bagus untuk driving traffic. Dipakai untuk menentukan 🔗 Most Clicked di Leaderboard. |

### Content Types per Platform

| Platform | Content Types | Keterangan |
|----------|--------------|------------|
| Instagram | Reel, Story, Carousel, Feed Post | Reel punya jangkauan terluas, Carousel punya engagement tertinggi |
| TikTok | Short Video, Duet, Stitch | Short Video dominan, Duet/Stitch untuk engagement komunitas |
| YouTube | Short, Long Video, Live | Shorts untuk jangkauan, Long Video untuk watch time & revenue |
| LinkedIn | Article, Post, Document | Document (carousel PDF) viral di LinkedIn, Article untuk SEO |

---

## Konfigurasi per Platform

Data dummy di-generate dengan parameter berbeda per platform supaya realistis:

| Parameter | Instagram | TikTok | YouTube | LinkedIn |
|-----------|-----------|--------|---------|----------|
| Base Followers | 45,200 | 28,500 | 12,800 | 8,900 |
| Daily Growth | +50 s/d +250 | +80 s/d +400 | +10 s/d +80 | +5 s/d +40 |
| Base Impressions | 15K – 35K | 25K – 80K | 5K – 20K | 3K – 12K |
| Engagement Multiplier | 6.5% | 8.0% | 4.5% | 5.5% |
| Posts/Week Target | 5 | 4 | 2 | 3 |
| Base Views | 8K – 25K | 20K – 100K | 3K – 15K | 2K – 8K |

**Kenapa TikTok paling tinggi?** TikTok punya algorithmic reach terbesar — bahkan akun kecil bisa mendapat jutaan views. Tapi followers-nya lebih rendah dari Instagram karena orang di TikTok lebih suka menonton daripada follow.

**Kenapa YouTube growth paling lambat?** Subscribe di YouTube adalah komitmen lebih besar daripada follow di platform lain. Tapi subscriber YouTube jauh lebih loyal dan engaged dalam jangka panjang.

---

## Hubungan Antar Data

```
generate_organic_data()  (daily × platform)
    │
    ├── followers, follower_growth
    │       → Cross-Channel Pulse (Ticker Tape)
    │       → Follower Growth Trend Chart
    │
    ├── impressions, likes, comments, shares, saves
    │       → North Star Ribbon (ER, SoV)
    │       → Metric Stack per Platform
    │       → Daily Engagement Rate Chart
    │       → Engagement Funnel (Reach → Interaction → Click)
    │
    ├── profile_visits, link_clicks
    │       → North Star Ribbon (Profile CVR)
    │       → Engagement Funnel (Click stage)
    │
    └── posts_published, posts_goal_weekly
            → North Star Ribbon (Consistency Score)

generate_content_library()  (per post)
    │
    ├── views, likes, comments, shares, saves, link_clicks
    │       → Content Library Grid & Table
    │
    ├── virality_score (shares + saves / views)
    │       → Content Library sorting
    │       → 🏆 Most Shared badge (Leaderboard)
    │
    └── conversion_score (link_clicks / views)
            → Content Library sorting
            → 🔗 Most Clicked badge (Leaderboard)
```

---

## Sumber Data di Production — Platform APIs

### Instagram Graph API
```
Base URL: https://graph.facebook.com/v18.0/
Auth: Facebook App + Instagram Business Account
Rate Limit: 200 calls/user/hour
Key Endpoints:
  GET /{ig-user-id}?fields=followers_count,media_count
  GET /{ig-user-id}/media?fields=timestamp,like_count,comments_count,impressions
  GET /{ig-media-id}/insights?metric=impressions,reach,saved,shares,video_views
```

### TikTok API for Business
```
Base URL: https://business-api.tiktok.com/open_api/v1.3/
Auth: OAuth 2.0 Access Token
Rate Limit: 600 calls/minute
Key Endpoints:
  GET /business/get/ → follower_count, likes_count
  GET /video/list/ → play_count, share_count, comment_count
  GET /video/query/ → per-video insights
```

### YouTube Data API v3
```
Base URL: https://www.googleapis.com/youtube/v3/
Auth: API Key + OAuth 2.0
Rate Limit: 10,000 units/day (quota-based)
Key Endpoints:
  GET /channels?part=statistics → subscriberCount, viewCount
  GET /videos?part=statistics → viewCount, likeCount, commentCount
  GET /analytics/reports → impressions, cardClicks (YouTube Analytics API)
```

### LinkedIn Marketing API
```
Base URL: https://api.linkedin.com/v2/
Auth: OAuth 2.0 (3-legged)
Rate Limit: 100,000 calls/day
Key Endpoints:
  GET /organizationalEntityFollowerStatistics → follower gains/losses
  GET /shares → per-post engagement metrics
  GET /organizationPageStatistics → page views, clicks
```

### Alternatif: Social Media Management Tools

Kalau klien tidak mau setup API per platform, bisa pakai aggregator:

| Tool | Platforms Supported | API? | Harga |
|------|-------------------|------|-------|
| **Sprout Social** | IG, TT, YT, LI, FB, X | Ya (export CSV/API) | $249/bulan |
| **Hootsuite** | IG, TT, YT, LI, FB, X | Ya (API) | $99/bulan |
| **Later** | IG, TT, LI, FB, Pinterest | Ya (export CSV) | $25/bulan |
| **Buffer** | IG, TT, YT, LI, FB, X | Ya (API) | $6/bulan |
| **Iconosquare** | IG, TT, LI, FB | Ya (API + export) | $49/bulan |

**Rekomendasi untuk klien Marktivo:** Mulai dengan **Buffer** ($6/bulan) untuk scheduling + basic analytics export. Upgrade ke **Sprout Social** kalau klien butuh API yang lebih granular.

---

## Catatan untuk Integrasi Production

| Dummy Function | Production Data Source | API / Method |
|---------------|----------------------|--------------|
| `generate_organic_data()` | Platform APIs (IG + TT + YT + LI) | Masing-masing API call per platform, lalu merge jadi satu DataFrame |
| `generate_content_library()` | Platform APIs (per-post metrics) | IG: `/media` endpoint · TT: `/video/list` · YT: `/videos` · LI: `/shares` |
| `engagement_rate` | Dihitung dari raw data | (Likes + Comments + Shares) ÷ Impressions × 100 |
| `share_of_voice` | Dihitung dari raw data | (Saves + Shares) ÷ Impressions × 100 |
| `profile_conversion_rate` | Dihitung dari raw data | Link Clicks ÷ Profile Visits × 100 |
| `virality_score` | Dihitung dari raw data | (Shares + Saves) ÷ Views × 100 |
| `conversion_score` | Dihitung dari raw data | Link Clicks ÷ Views × 100 |
