//import { rename } from 'templates/home.py';
function toggleBorder() {
    var border = document.getElementById("border");
    border.classList.toggle("hidden");
    if (!border.classList.contains("hidden")) {
        border.style.right = "0"; // 显示导航栏时将其移到屏幕内
    }
}

// 关闭导航栏
function closeBorder() {
    var border = document.getElementById("border");
    border.classList.add("hidden");
    border.style.right = "-400px"; // 将导航栏移出屏幕外
}



// 修改用户名
// 修改用户名


// 执行退出操作
