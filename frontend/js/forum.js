const newPostLink = document.getElementById("btn-new-post");
if (newPostLink) {
    newPostLink.addEventListener("click", (e) => {
        e.preventDefault();
        window.navigateTo("/novo_post");
    });
}