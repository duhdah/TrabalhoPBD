CREATE DATABASE pet ;

\c pet;

CREATE TABLE Reuniao_Ata (
    codigo INTEGER PRIMARY KEY,
    texto TEXT NOT NULL,
    assunto VARCHAR(200) NOT NULL,
    data DATE NOT NULL,
    numero INTEGER NOT NULL,
    coordenador VARCHAR(80) NOT NULL,
    redator VARCHAR(80) NOT NULL
);

CREATE TABLE Membro_Equipe (
    matricula VARCHAR(15) PRIMARY KEY,
    nomeCompleto VARCHAR(80) NOT NULL,
    dataIngresso DATE NOT NULL
);

CREATE TABLE Reuniao_Membro (
    codigo INTEGER,
    matricula VARCHAR(15),

    PRIMARY KEY (codigo, matricula),

    FOREIGN KEY (codigo)
        REFERENCES Reuniao_Ata(codigo),

    FOREIGN KEY (matricula)
        REFERENCES Membro_Equipe(matricula)
);

CREATE TABLE Petiano (
    matricula VARCHAR(15) PRIMARY KEY,
    curso VARCHAR(50) NOT NULL,
    semestre VARCHAR(10) NOT NULL,

    FOREIGN KEY (matricula)
        REFERENCES Membro_Equipe(matricula)
);

CREATE TABLE Tutor (
    matricula VARCHAR(15) PRIMARY KEY,
    dataFimGestao DATE NOT NULL,

    FOREIGN KEY (matricula)
        REFERENCES Membro_Equipe(matricula)
);

CREATE TABLE Projeto (
    nomeProjeto VARCHAR(100) PRIMARY KEY,
    matriculaLider VARCHAR(15) NOT NULL,
    descricao TEXT,
    status VARCHAR(30) NOT NULL,
    codigoCobalto VARCHAR(50) NOT NULL,

    FOREIGN KEY (matriculaLider)
        REFERENCES Petiano(matricula)
);

CREATE TABLE Reuniao_Projeto (
    codigo INTEGER,
    nomeProjeto VARCHAR(100),

    PRIMARY KEY (codigo, nomeProjeto),

    FOREIGN KEY (codigo)
        REFERENCES Reuniao_Ata(codigo),

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto(nomeProjeto)
);

CREATE TABLE Projeto_Extensao (
    nomeProjeto VARCHAR(100) PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto(nomeProjeto)
);

CREATE TABLE Membro_Externo (
    nomeInstituicao VARCHAR(100) PRIMARY KEY,
    endereco VARCHAR(150),
    publicoAtendido TEXT,
    nomeResponsavel VARCHAR(80),
    telefone VARCHAR(20)
);

CREATE TABLE MembroExterno_ProjetoExtensao (
    nomeInstituicao VARCHAR(100),
    nomeProjeto VARCHAR(100),

    PRIMARY KEY (nomeInstituicao, nomeProjeto),

    FOREIGN KEY (nomeInstituicao)
        REFERENCES Membro_Externo(nomeInstituicao),

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto_Extensao(nomeProjeto)
);

CREATE TABLE Evento (
    nomeProjeto VARCHAR(100) PRIMARY KEY,
    dataEvento DATE NOT NULL,
    duracao INTEGER CHECK (duracao > 0),

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto_Extensao(nomeProjeto)
);

CREATE TABLE Projeto_Ensino (
    nomeProjeto VARCHAR(100) PRIMARY KEY,
    topico VARCHAR(100) NOT NULL,

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto(nomeProjeto)
);

CREATE TABLE Aluno (
    matriculaAluno VARCHAR(15) PRIMARY KEY,
    curso VARCHAR(50) NOT NULL
);

CREATE TABLE Projeto_Aluno (
    nomeProjeto VARCHAR(100),
    matriculaAluno VARCHAR(15),

    PRIMARY KEY (nomeProjeto, matriculaAluno),

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto_Ensino(nomeProjeto),

    FOREIGN KEY (matriculaAluno)
        REFERENCES Aluno(matriculaAluno)
);

CREATE TABLE Projeto_Pesquisa (
    nomeProjeto VARCHAR(100) PRIMARY KEY,
    area VARCHAR(100) NOT NULL,

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto(nomeProjeto)
);

CREATE TABLE Artigo_Cientifico (
    codigoArtigo INTEGER PRIMARY KEY,
    congresso VARCHAR(100) NOT NULL,
    status VARCHAR(30) CHECK (status IN ('Submetido', 'Aceito', 'Rejeitado', 'Publicado'))
);

CREATE TABLE Projeto_Artigo (
    nomeProjeto VARCHAR(100),
    codigoArtigo INTEGER,

    PRIMARY KEY (nomeProjeto, codigoArtigo),

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto_Pesquisa(nomeProjeto),

    FOREIGN KEY (codigoArtigo)
        REFERENCES Artigo_Cientifico(codigoArtigo)
);

CREATE TABLE Historico (
    semestre VARCHAR(10),
    matricula VARCHAR(15),
    reprovacoes INTEGER NOT NULL,

    PRIMARY KEY (semestre, matricula),

    FOREIGN KEY (matricula)
        REFERENCES Petiano(matricula)
);

CREATE TABLE Projeto_Petiano (
    nomeProjeto VARCHAR(100),
    matricula VARCHAR(15),

    PRIMARY KEY (nomeProjeto, matricula),

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto(nomeProjeto),

    FOREIGN KEY (matricula)
        REFERENCES Petiano(matricula)
);

-- Preenchendo alguns dados nas tabelas

INSERT INTO Membro_Equipe VALUES
('24101555', 'Ana Souza', '2025-03-01'),
('24206152', 'Bruno Lima', '2023-04-10'),
('15265252', 'Carla Martins', '2024-01-15'),
('24526484', 'Daniel Rocha', '2022-08-20'),
('21458555', 'Eduarda Silva', '2021-02-01');

INSERT INTO Petiano VALUES
('24101555', 'Ciencia da Computacao', '5'),
('24206152', 'Ciencia da Computacao', '4'),
('21458555', 'Engenharia da Computacao', '3');

INSERT INTO Tutor VALUES
('15265252', '2028-12-31'),
('24526484', '2027-12-31');

INSERT INTO Reuniao_Ata VALUES
(1565, 'Falas e decisões.', 'Discussao sobre andamento dos projetos.', '2026-03-10', 15, 'Carla Martins', 'Bruno Lima'),
(2425, 'Texto detalhado da reunião', 'Planejamento do evento de extensao.', '2026-04-02', 16, 'Daniel Rocha', 'Ana Souza');

INSERT INTO Reuniao_Membro VALUES
(1565, '15265252'),
(1565, '24206152'),
(1565, '21458555'),
(2425, '24526484'),
(2425, '24101555');

INSERT INTO Projeto VALUES
('PETCode', '24101555', 'Projeto de oficinas de programacao', 'Ativo', '7801'),
('PETEnsina', '24206152', 'Projeto de aulas de Pensamento Computacional', 'Ativo', '2502'),
('PETPesquisaIA', '21458555', 'Pesquisa em IA aplicada', 'Ativo', '5303');

INSERT INTO Reuniao_Projeto VALUES
(1565, 'PETEnsina'),
(1565, 'PETCode'),
(1565, 'PETPesquisaIA'),
(2425, 'PETEnsina');

INSERT INTO Projeto_Extensao VALUES
('PETEnsina', 'Oficinas para escolas');

INSERT INTO Membro_Externo VALUES
('Escola Municipal Pelotas', 'Rua Central 100', 'Alunos do ensino fundamental', 'Mariana Costa', '(53)99999-1111'),
('IFSul', 'Av. Bento 500', 'Estudantes de tecnologia', 'Ricardo Alves', '(53)99999-2222');

INSERT INTO MembroExterno_ProjetoExtensao VALUES
('Escola Municipal Pelotas', 'PETEnsina'),
('IFSul', 'PETEnsina');

INSERT INTO Evento VALUES
--('PETEnsina', '2026-05-15', 2),
('PETEnsina', '2026-02-27', 4);

INSERT INTO Projeto_Ensino VALUES
('PETEnsina', 'Estruturas de Dados');

INSERT INTO Aluno VALUES
('25685742', 'Ciencia da Computacao'),
('24206174', 'Ciencia da Computacao'),
('12634578', 'Engenharia da Computacao');

INSERT INTO Projeto_Aluno VALUES
('PETEnsina', '25685742'),
('PETEnsina', '24206174'),
('PETEnsina', '12634578');

INSERT INTO Projeto_Pesquisa VALUES
('PETPesquisaIA', 'Inteligencia Artificial');

INSERT INTO Artigo_Cientifico VALUES
(101, 'SBC', 'Aceito'),
(102, 'WEI', 'Submetido');

INSERT INTO Projeto_Artigo VALUES
('PETPesquisaIA', 101),
('PETPesquisaIA', 102);

INSERT INTO Historico VALUES
('2025/1', '24101555', 0),
('2025/1', '21458555', 1),
('2025/1', '24206152', 1),
('2025/2', '24206152', 1);

INSERT INTO Projeto_Petiano VALUES
('PETCode', '24101555'),
('PETCode', '21458555'),
('PETEnsina', '21458555'),
('PETPesquisaIA', '24206152');


ALTER TABLE Artigo_Cientifico
ADD COLUMN titulo VARCHAR(200);

ALTER TABLE Artigo_Cientifico
ADD COLUMN matriculaAutor VARCHAR(15);

ALTER TABLE Artigo_Cientifico
ADD CONSTRAINT fk_autor
FOREIGN KEY (matriculaAutor)
REFERENCES Petiano(matricula);

INSERT INTO Artigo_Cientifico VALUES
    (103, 'SBIE', 'Aceito', 'Artigo 1', '24101555'),
    (104, 'WEI', 'Submetido', 'Artigo 2', '24101555'),
    (105, 'WEI', 'Publicado', 'Artigo 3', '21458555');

INSERT INTO Projeto_Artigo VALUES
    ('PETPesquisaIA', 101),
    ('PETPesquisaIA', 102);

INSERT INTO Projeto VALUES
    ('Curso dos Idosos', '24206152', 'Inclusão digital para idosos', 'Ativo', '5406');
	
INSERT INTO Projeto_Extensao VALUES
    ('Curso dos Idosos', 'Inclusão digital para idosos');

--- novidade: adicionei on update cascade para permitir mudança de nome de projeto
ALTER TABLE Reuniao_Projeto 
    DROP CONSTRAINT reuniao_projeto_nomeprojeto_fkey;

ALTER TABLE Reuniao_Projeto 
    ADD CONSTRAINT nomeProjeto_fkey 
    FOREIGN KEY (nomeProjeto) REFERENCES Projeto(nomeProjeto) 
    ON UPDATE CASCADE ON DELETE CASCADE;
	
ALTER TABLE Projeto_Ensino DROP CONSTRAINT IF EXISTS projeto_ensino_nomeprojeto_fkey;
ALTER TABLE Projeto_Ensino 
    ADD CONSTRAINT nomeProjeto_fkey 
    FOREIGN KEY (nomeProjeto) REFERENCES Projeto(nomeProjeto) 
    ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE Projeto_Pesquisa DROP CONSTRAINT IF EXISTS projeto_pesquisa_nomeprojeto_fkey;
ALTER TABLE Projeto_Pesquisa 
    ADD CONSTRAINT nomeProjeto_fkey 
    FOREIGN KEY (nomeProjeto) REFERENCES Projeto(nomeProjeto) 
    ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE Projeto_Extensao DROP CONSTRAINT IF EXISTS projeto_extensao_nomeprojeto_fkey;
ALTER TABLE Projeto_Extensao 
    ADD CONSTRAINT nomeProjeto_fkey 
    FOREIGN KEY (nomeProjeto) REFERENCES Projeto(nomeProjeto) 
    ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE Projeto_Petiano DROP CONSTRAINT IF EXISTS projeto_petiano_nomeprojeto_fkey;
ALTER TABLE Projeto_Petiano 
    ADD CONSTRAINT nomeProjeto_fkey 
    FOREIGN KEY (nomeProjeto) REFERENCES Projeto(nomeProjeto) 
    ON UPDATE CASCADE ON DELETE CASCADE;

