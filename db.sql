CREATE TABLE IF NOT EXISTS "usuarios" (
	"id" SERIAL NOT NULL,
	"apelido" VARCHAR(16) NOT NULL,
	"hash_senha" TEXT NOT NULL,
	"link_avatar" TEXT NOT NULL,
	"biografia" TEXT NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	UNIQUE ("apelido")
);

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

CREATE TABLE IF NOT EXISTS "mensagens" (
	"id" SERIAL NOT NULL,
	"autor_id" INTEGER NOT NULL,
	"mensagem" TEXT NOT NULL,
	"timestamp" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	CONSTRAINT "mensagens_autor_id_fk" FOREIGN KEY ("autor_id") REFERENCES "usuarios" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE INDEX "idx_mensagens_autor_id" ON "mensagens" ("autor_id");