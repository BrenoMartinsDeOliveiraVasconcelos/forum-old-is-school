--
-- PostgreSQL database dump
--

\restrict 5pDHjFaEQ9zMtBnlqkGNLqQFzTUsK5zBYz1R02fHSo9uzYgOoNz4AdjHi1f6KX9

-- Dumped from database version 17.6 (Debian 17.6-0+deb13u1)
-- Dumped by pg_dump version 17.6 (Debian 17.6-0+deb13u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: categorias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categorias (
    id integer NOT NULL,
    titulo character varying(32) NOT NULL,
    "desc" character varying(128) NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    deletado boolean DEFAULT false NOT NULL
);


ALTER TABLE public.categorias OWNER TO postgres;

--
-- Name: categorias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categorias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categorias_id_seq OWNER TO postgres;

--
-- Name: categorias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categorias_id_seq OWNED BY public.categorias.id;


--
-- Name: comentarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comentarios (
    id integer NOT NULL,
    autor_id integer NOT NULL,
    post_id integer NOT NULL,
    conteudo text NOT NULL,
    "timestamp" timestamp with time zone DEFAULT now() NOT NULL,
    deletado boolean DEFAULT false NOT NULL
);


ALTER TABLE public.comentarios OWNER TO postgres;

--
-- Name: comentarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comentarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comentarios_id_seq OWNER TO postgres;

--
-- Name: comentarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comentarios_id_seq OWNED BY public.comentarios.id;


--
-- Name: curtidas_comentarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.curtidas_comentarios (
    id integer NOT NULL,
    autor_id integer NOT NULL,
    comentario_id integer NOT NULL,
    deletado boolean DEFAULT false NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.curtidas_comentarios OWNER TO postgres;

--
-- Name: curtidas_comentarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.curtidas_comentarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.curtidas_comentarios_id_seq OWNER TO postgres;

--
-- Name: curtidas_comentarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.curtidas_comentarios_id_seq OWNED BY public.curtidas_comentarios.id;


--
-- Name: curtidas_posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.curtidas_posts (
    id integer NOT NULL,
    autor_id integer NOT NULL,
    post_id integer NOT NULL,
    deletado boolean DEFAULT false NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.curtidas_posts OWNER TO postgres;

--
-- Name: curtidas_posts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.curtidas_posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.curtidas_posts_id_seq OWNER TO postgres;

--
-- Name: curtidas_posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.curtidas_posts_id_seq OWNED BY public.curtidas_posts.id;


--
-- Name: mensagens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mensagens (
    id integer NOT NULL,
    autor_id integer NOT NULL,
    mensagem text NOT NULL,
    "timestamp" timestamp with time zone DEFAULT now() NOT NULL,
    deletado boolean DEFAULT false NOT NULL
);


ALTER TABLE public.mensagens OWNER TO postgres;

--
-- Name: mensagens_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mensagens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mensagens_id_seq OWNER TO postgres;

--
-- Name: mensagens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mensagens_id_seq OWNED BY public.mensagens.id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.posts (
    id integer NOT NULL,
    autor_id integer NOT NULL,
    titulo character varying(32) NOT NULL,
    conteudo text NOT NULL,
    "timestamp" timestamp with time zone DEFAULT now() NOT NULL,
    deletado boolean DEFAULT false NOT NULL,
    midia text,
    mural boolean DEFAULT false NOT NULL,
    categoria_id integer
);


ALTER TABLE public.posts OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.posts_id_seq OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    apelido character varying(16) NOT NULL,
    hash_senha text NOT NULL,
    avatar_filename text,
    biografia text,
    deletado boolean DEFAULT false NOT NULL,
    assinatura character varying(128),
    admin boolean DEFAULT false NOT NULL
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: categorias id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias ALTER COLUMN id SET DEFAULT nextval('public.categorias_id_seq'::regclass);


--
-- Name: comentarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comentarios ALTER COLUMN id SET DEFAULT nextval('public.comentarios_id_seq'::regclass);


--
-- Name: curtidas_comentarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curtidas_comentarios ALTER COLUMN id SET DEFAULT nextval('public.curtidas_comentarios_id_seq'::regclass);


--
-- Name: curtidas_posts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curtidas_posts ALTER COLUMN id SET DEFAULT nextval('public.curtidas_posts_id_seq'::regclass);


--
-- Name: mensagens id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mensagens ALTER COLUMN id SET DEFAULT nextval('public.mensagens_id_seq'::regclass);


--
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Name: categorias categorias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_pkey PRIMARY KEY (id);


--
-- Name: categorias categorias_titulo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_titulo_key UNIQUE (titulo);


--
-- Name: comentarios comentarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comentarios
    ADD CONSTRAINT comentarios_pkey PRIMARY KEY (id);


--
-- Name: curtidas_comentarios curtidas_comentarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curtidas_comentarios
    ADD CONSTRAINT curtidas_comentarios_pkey PRIMARY KEY (id);


--
-- Name: curtidas_posts curtidas_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curtidas_posts
    ADD CONSTRAINT curtidas_posts_pkey PRIMARY KEY (id);


--
-- Name: mensagens mensagens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mensagens
    ADD CONSTRAINT mensagens_pkey PRIMARY KEY (id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_apelido_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_apelido_key UNIQUE (apelido);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: idx_comentarios_autor_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_comentarios_autor_id ON public.comentarios USING btree (autor_id);


--
-- Name: idx_comentarios_post_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_comentarios_post_id ON public.comentarios USING btree (post_id);


--
-- Name: idx_mensagens_autor_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_mensagens_autor_id ON public.mensagens USING btree (autor_id);


--
-- Name: idx_posts_autor_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_posts_autor_id ON public.posts USING btree (autor_id);


--
-- Name: curtidas_comentarios autor_id_curtidas_comentarios_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curtidas_comentarios
    ADD CONSTRAINT autor_id_curtidas_comentarios_fk FOREIGN KEY (autor_id) REFERENCES public.usuarios(id);


--
-- Name: curtidas_posts autor_id_curtidas_posts_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curtidas_posts
    ADD CONSTRAINT autor_id_curtidas_posts_fk FOREIGN KEY (autor_id) REFERENCES public.usuarios(id);


--
-- Name: posts categoria_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT categoria_id_fk FOREIGN KEY (categoria_id) REFERENCES public.categorias(id);


--
-- Name: curtidas_comentarios comentario_id_curtidas_comentarios_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curtidas_comentarios
    ADD CONSTRAINT comentario_id_curtidas_comentarios_fk FOREIGN KEY (comentario_id) REFERENCES public.comentarios(id);


--
-- Name: comentarios comentarios_autor_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comentarios
    ADD CONSTRAINT comentarios_autor_id_fk FOREIGN KEY (autor_id) REFERENCES public.usuarios(id);


--
-- Name: comentarios comentarios_post_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comentarios
    ADD CONSTRAINT comentarios_post_id_fk FOREIGN KEY (post_id) REFERENCES public.posts(id);


--
-- Name: mensagens mensagens_autor_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mensagens
    ADD CONSTRAINT mensagens_autor_id_fk FOREIGN KEY (autor_id) REFERENCES public.usuarios(id);


--
-- Name: curtidas_posts post_id_curtidas_posts_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.curtidas_posts
    ADD CONSTRAINT post_id_curtidas_posts_fk FOREIGN KEY (post_id) REFERENCES public.posts(id);


--
-- Name: posts posts_autor_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_autor_id_fk FOREIGN KEY (autor_id) REFERENCES public.usuarios(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 5pDHjFaEQ9zMtBnlqkGNLqQFzTUsK5zBYz1R02fHSo9uzYgOoNz4AdjHi1f6KX9

