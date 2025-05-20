const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { exec } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 3000;
const DOWNLOAD_FOLDER = path.join(__dirname, "downloads");

if (!fs.existsSync(DOWNLOAD_FOLDER)) {
  fs.mkdirSync(DOWNLOAD_FOLDER);
}

app.use(cors());
app.use(bodyParser.json());

app.post("/api/download", (req, res) => {
  const { url, format } = req.body;

  if (!url || !format) {
    return res.status(400).json({ error: "Missing url or format" });
  }

  const outputTemplate = path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s");
  let command = `yt-dlp -o "${outputTemplate}" ${url}`;

  if (format === "mp3") {
    command += " --extract-audio --audio-format mp3";
  }

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error("Download error:", error);
      return res.status(500).json({ error: "Download failed" });
    }

    // Find the latest file in the download folder
    const files = fs.readdirSync(DOWNLOAD_FOLDER)
      .map(name => ({
        name,
        time: fs.statSync(path.join(DOWNLOAD_FOLDER, name)).mtime.getTime()
      }))
      .sort((a, b) => b.time - a.time);

    if (files.length === 0) {
      return res.status(500).json({ error: "No file found" });
    }

    const filename = files[0].name;
    const filepath = path.join(DOWNLOAD_FOLDER, filename);

    res.download(filepath, filename, err => {
      if (err) {
        console.error("Send file error:", err);
        res.status(500).json({ error: "Failed to send file" });
      }

      // Optional: Delete file after sending
      fs.unlink(filepath, () => {});
    });
  });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
