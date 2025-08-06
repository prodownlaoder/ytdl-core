// main.js
require('dotenv').config();
const express = require('express');
const ytdl = require('ytdl-core');

const app = express();
const PORT = 3000;

app.use(express.json());

app.get('/api/info', async (req, res) => {
  const videoURL = req.query.url;

  if (!videoURL || !ytdl.validateURL(videoURL)) {
    return res.status(400).json({ error: '❌ Invalid or missing YouTube URL.' });
  }

  try {
    console.log(`🔍 Fetching metadata for: ${videoURL}`);

    const options = {
      requestOptions: {
        headers: {
          cookie: process.env.YOUTUBE_COOKIE || ""
        }
      }
    };

    const info = await ytdl.getBasicInfo(videoURL, options);
    const details = info.videoDetails;

    const bestThumbnail = details.thumbnails.reduce((prev, current) => {
      return current.width > prev.width ? current : prev;
    });

    const durationMinutes = (parseInt(details.lengthSeconds || 0) / 60).toFixed(2);

    const data = {
      title: details.title,
      author: details.author.name,
      thumbnail: bestThumbnail.url,
      durationMinutes: parseFloat(durationMinutes),
      views: parseInt(details.viewCount || 0),
    };

    console.log(`✅ Sent metadata for: "${details.title}"`);
    res.json(data);
  } catch (err) {
    console.error('❌ Failed to fetch metadata:', err.message);
    res.status(500).json({ error: 'Failed to fetch metadata', details: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 YouTube metadata API running at http://localhost:${PORT}`);
});
