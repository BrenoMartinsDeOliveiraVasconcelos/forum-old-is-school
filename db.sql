-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           PostgreSQL 17.6 (Debian 17.6-1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.3.0-5) 14.3.0, 64-bit
-- OS do Servidor:               
-- HeidiSQL Versão:              12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES  */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Copiando estrutura para tabela public.usuarios
CREATE TABLE IF NOT EXISTS "usuarios" (
	"id" SERIAL NOT NULL,
	"apelido" VARCHAR(16) NOT NULL,
	"hash_senha" TEXT NOT NULL,
	"link_avatar" TEXT NOT NULL,
	"biografia" TEXT NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	UNIQUE ("apelido")
);

-- Copiando estrutura para tabela public.posts
CREATE TABLE IF NOT EXISTS "posts" (
	"id" SERIAL NOT NULL,
	"autor_id" INTEGER NOT NULL,
	"titulo" VARCHAR(32) NOT NULL,
	"conteudo" TEXT NOT NULL,
	"timestamp" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	CONSTRAINT "posts_autor_id_fk" FOREIGN KEY ("autor_id") REFERENCES "usuarios" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE INDEX "idx_posts_autor_id" ON "posts" ("autor_id");

-- Copiando estrutura para tabela public.comentarios
CREATE TABLE IF NOT EXISTS "comentarios" (
	"id" SERIAL NOT NULL,
	"autor_id" INTEGER NOT NULL,
	"post_id" INTEGER NOT NULL,
	"conteudo" TEXT NOT NULL,
	"timestamp" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	CONSTRAINT "comentarios_autor_id_fk" FOREIGN KEY ("autor_id") REFERENCES "usuarios" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "comentarios_post_id_fk" FOREIGN KEY ("post_id") REFERENCES "posts" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE INDEX "idx_comentarios_post_id" ON "comentarios" ("post_id");
CREATE INDEX "idx_comentarios_autor_id" ON "comentarios" ("autor_id");

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela public.mensagens
CREATE TABLE IF NOT EXISTS "mensagens" (
	"id" SERIAL NOT NULL,
	"autor_id" INTEGER NOT NULL,
	"mensagem" TEXT NOT NULL,
	"timestamp" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	CONSTRAINT "mensagens_autor_id_fk" FOREIGN KEY ("autor_id") REFERENCES "usuarios" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE INDEX "idx_mensagens_autor_id" ON "mensagens" ("autor_id");

-- Exportação de dados foi desmarcado.

-- Exportação de dados foi desmarcado.

-- Exportação de dados foi desmarcado.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
