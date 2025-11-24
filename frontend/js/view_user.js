import { buscarUsuario, formatarData, buscarAvatar } from "./funcoes.js";

const hash = window.location.hash;
const parts = hash.split("/");
const id = parts[2];


const user = await buscarUsuario(id);
console.log(user);

document.getElementById("name").innerText = user.usuarios[0].apelido;
document.getElementById("biografia").innerText = user.usuarios[0].biografia ;
document.getElementById("assinatura").innerText = user.usuarios[0].assinatura;
document.getElementById("avatar_view").src = buscarAvatar(user.usuarios[0].avatar_filename);

const divUserPosts = document.getElementById('posts-user');

user.usuarios[0].posts.posts.forEach(post => {
    const divPost = document.createElement('div');
    divPost.classList.add("post");

    divPost.innerHTML = `
        <h3>${post.titulo}</h3>
        <p class="post-meta">Postado em <b>${formatarData(post.timestamp)}</b></p>
        <a href="#/posts/${post.id}" class="post-link text-end d-block">Visualizar >></a>
    `;
    divUserPosts.appendChild(divPost);
});