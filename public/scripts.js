// const axios = require("./axios");
// const utils = require('./get_list.js')

document.addEventListener('DOMContentLoaded', function () {
    const categoryNav = document.getElementById('category-nav');
    const videoList = document.getElementById('video-list');

    function fetchVideos(category) {
        // 清除之前的视频列表
        videoList.innerHTML = '';
        var url = "https://app-v1.ecoliving168.com/api/v1/movie/screen/list"
        var par = get_list_params("1");
        var pack = getpack(par)
        var signature = HMACEncrypt(pack)
        console.log(pack, '\n', signature);
        // 发送请求到后端获取视频列表
        axios.get(url, {
            params: {
                pack: pack,
                signature: signature
            }
        })
            .then(response => {
                console.log(JSON.stringify(response.data.data));
            })
            .catch(error => {
                console.error('Error:', error);
            });
        // fetch(`/api/videos?category=${category}`)
        //     .then(response => response.json())
        //     .then(data => {
        //         // 假设后端返回的数据是一个包含视频对象的数组
        //         data.forEach(video => {
        //             const li = document.createElement('li');
        //             li.textContent = video.title; // 可以根据需要添加更多信息，如视频描述、链接等
        //             videoList.appendChild(li);
        //         });
        //     })
        //     .catch(error => {
        //         console.error('获取视频列表失败:', error);
        //     });
    }

    // 默认加载所有视频（可以根据需要修改）
    fetchVideos('all');

    // 添加分类按钮事件监听器
    categoryNav.addEventListener('click', function (event) {
        if (event.target.tagName === 'BUTTON') {
            const category = event.target.dataset.category;
            fetchVideos(category);
        }
    });
});
