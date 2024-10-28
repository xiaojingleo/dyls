const express = require('express');
const app = express();
const PORT = 3000;

// 模拟的视频数据
const videos = [
    { id: 1, title: '电影1', category: '电影' },
    { id: 2, title: '电影2', category: '电影' },
    { id: 3, title: '电视剧1', category: '电视剧' },
    // ... 其他视频数据
];

// 路由处理函数
app.get('/api/videos', (req, res) => {
    const category = req.query.category || 'all';
    let filteredVideos = videos;

    if (category !== 'all') {
        filteredVideos = videos.filter(video => video.category === category);
    }

    res.json(filteredVideos);
});

// 启动服务器
app.listen(PORT, () => {
    console.log('server is running on port 3000');
});
