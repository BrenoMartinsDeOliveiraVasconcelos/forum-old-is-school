import { buscarUsuario, formatarData } from "./funcoes.js";

const hash = window.location.hash;
const parts = hash.split("/");
const id = parts[2];


const user = await buscarUsuario(id);
console.log(user);

document.getElementById("name").value = user.usuarios[0].apelido;
document.getElementById("assinatura").value = user.usuarios[0].assinatura;

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