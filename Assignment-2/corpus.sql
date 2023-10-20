-- Table: public.terms

-- DROP TABLE IF EXISTS public.terms;

CREATE TABLE IF NOT EXISTS public.terms
(
    term text COLLATE pg_catalog."default" NOT NULL,
    num_chars integer NOT NULL,
    CONSTRAINT terms_pkey PRIMARY KEY (term)
);

CREATE TABLE IF NOT EXISTS public.term_count
(
    countdoc integer NOT NULL,
    countterm text COLLATE pg_catalog."default" NOT NULL,
    count integer NOT NULL,
    CONSTRAINT term_count_pkey PRIMARY KEY (countdoc, countterm),
    CONSTRAINT document_id FOREIGN KEY (countdoc)
        REFERENCES public.documents (docid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT term FOREIGN KEY (countterm)
        REFERENCES public.terms (term) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

CREATE TABLE IF NOT EXISTS public.documents
(
    docid integer NOT NULL,
    doctitle text COLLATE pg_catalog."default" NOT NULL,
    doctext text COLLATE pg_catalog."default" NOT NULL,
    num_chars integer NOT NULL,
    docdate date NOT NULL,
    doccat integer NOT NULL,
    CONSTRAINT documents_pkey PRIMARY KEY (docid),
    CONSTRAINT category_id FOREIGN KEY (doccat)
        REFERENCES public.category (catid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE IF NOT EXISTS public.category
(
    catid integer NOT NULL,
    catname text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT category_pkey PRIMARY KEY (catid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.terms
    OWNER to postgres;