import { buscarPost, buscarUsuario, formatarData, customAlert } from "./funcoes.js";

const hash = window.location.hash;
const postId = hash.split("/")[2];

try {
  async function carregarPost() {
    const postData = await buscarPost(postId);
    console.log(postData);

    const autor = await buscarUsuario(postData.posts[0].autor_id);

    console.log(autor);


    const post = {
      titulo: postData.posts[0].titulo,
      conteudo: postData.posts[0].conteudo,
      data: formatarData(postData.posts[0].timestamp),
      autor: autor.usuarios[0].apelido
    };

    document.getElementById('postsContainer').innerHTML = `
      <h1>${post.titulo}</h1>
      <h6>Postado em ${post.data} por ${post.autor}</h6> <br>
      ${marked.parse(post.conteudo)}
    `;

    document.getElementById('post-votes-value').innerHTML = ' 0';
    document.getElementById('post-comments-value').innerHTML = ' 0';
  }


  carregarPost();
} catch (error) {

}


