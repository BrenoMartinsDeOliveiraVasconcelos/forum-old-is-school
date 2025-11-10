const postLink = document.querySelectorAll(".post-link");
if (postLink) {
    postLink.addEventListener("click", (e) => {
        e.preventDefault();
        window.navigateTo("/post/1234");
    });
}