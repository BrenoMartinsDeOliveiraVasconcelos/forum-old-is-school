const post = {
      titulo: "Guia de Montagem de PCs Antigos",
      conteudo: `
## 💡 Introdução

Montar um PC antigo pode ser um passatempo nostálgico e educativo.  
Além de resgatar a história da computação pessoal, é uma ótima forma de entender como o hardware evoluiu ao longo dos anos.  

Neste guia, vou mostrar como identificar, montar e testar componentes clássicos — daqueles que faziam barulho ao ligar e tinham LEDs piscando no gabinete. 😄

## 🧩 1. Identificando os Componentes

Antes de começar, é importante saber de qual época é o computador que você quer montar.  
As gerações mais populares entre colecionadores são:

- **Anos 90** (Socket 7 / Pentium MMX / K6-2)  
  Placas-mãe com conectores IDE e disquete.

- **Início dos 2000** (Pentium III / Athlon XP)  
  Memórias SDRAM ou DDR1 e fontes ATX 20 pinos.

- **Era dos “gabinetes beige”** — quando tudo era bege e pesado. 😅

**Dica:** verifique se a placa-mãe ainda possui bateria CMOS funcional e capacitores em bom estado.

## 🪛 2. Montagem Passo a Passo

**Limpeza:**  
Use pincel macio e álcool isopropílico para remover poeira e oxidação.

**Fonte de alimentação:**  
Fontes AT antigas podem ser perigosas; teste com um multímetro antes de ligar.

**Processador e cooler:**  
Aplique uma fina camada de pasta térmica (mesmo os antigos precisam disso).

**Memória RAM:**  
Encaixe com cuidado, pois os slots antigos são frágeis.

**Placa de vídeo:**  
AGP, PCI ou até ISA — cada uma tem seu charme.

## 💾 3. Sistema Operacional

Sistemas clássicos que funcionam bem nesses PCs:

- MS-DOS 6.22
- Windows 95 / 98 / ME
- Windows 2000 / XP (em máquinas mais “modernas”)
- Distribuições Linux antigas (Slackware, Debian 3.0)

Para testar hardware, recomendo ferramentas como **MemTest86** e **HDD Regenerator** (se o HD ainda estiver vivo 😅).

## 🧠 4. Curiosidades

- Alguns PCs dos anos 90 tinham **chave turbo**, que só mudava o número no display!
- Placas de som **Sound Blaster 16** ainda são cobiçadas por entusiastas de jogos retrô.
- A BIOS de muitos modelos antigos pode ser atualizada via disquete.

## 🗨️ Conclusão

Montar um PC antigo é mais do que um hobby — é uma viagem no tempo.  
Além de reaprender conceitos básicos de hardware, você revive uma época em que a inicialização do Windows 98 era motivo de alegria. 😄

Se quiser compartilhar suas montagens, poste fotos, modelos de peças e resultados de benchmark — é assim que a comunidade cresce!
`
    };

    document.getElementById('postsContainer').innerHTML = `
      <h1>${post.titulo}</h1>
      <h6>Postado em 10/11/2025 por Lucas Ferreira</h6> <br>
      ${marked.parse(post.conteudo)}
    `;