import { buscarUsuario } from "./funcoes.js";

const hash = window.location.hash;
const parts = hash.split("/");
const id = parts[2];


const user = await buscarUsuario(id);
console.log(user);

document.getElementById("name").value = user.usuarios[0].apelido;
document.getElementById("assinatura").value = user.usuarios[0].assinatura;
