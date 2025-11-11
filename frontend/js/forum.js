const newPostLink = document.getElementById("btn-new-post");
console.log(newPostLink);

if (newPostLink) {
    newPostLink.addEventListener("click", (e) => {
        e.preventDefault();
        window.navigateTo("/novo_post");
    });
}