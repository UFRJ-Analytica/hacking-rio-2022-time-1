SET check_function_bodies = false;

CREATE TABLE tartaruga(
  identificador serial NOT NULL,
  nome varchar NOT NULL,
  ultimo_encontro date,
  forma varchar NOT NULL,
  CONSTRAINT tartaruga_pkey PRIMARY KEY(identificador)
);

COMMENT ON TABLE tartaruga IS 'tabela para a identificacao de tartarugas';

CREATE TABLE encontro(
  identificador serial NOT NULL,
  latitude varchar NOT NULL,
  longitude varchar NOT NULL,
  tartaruga_identificador integer NOT NULL,
  imagem_corpo bytea NOT NULL,
  imagem_cabeca bytea NOT NULL,
  "data" date NOT NULL,
  CONSTRAINT encontro_pkey PRIMARY KEY(identificador)
);

COMMENT ON TABLE encontro IS 'tabela dos encontros de tartarugas';

ALTER TABLE encontro
  ADD CONSTRAINT encontro_tartaruga_identificador_fkey
    FOREIGN KEY (tartaruga_identificador) REFERENCES tartaruga (identificador);