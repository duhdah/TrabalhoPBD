CREATE DATABASE pet;

\c pet;

CREATE TABLE Membro_Equipe (
    matricula VARCHAR(15) PRIMARY KEY,
    nomeCompleto VARCHAR(80) NOT NULL,
    dataIngresso DATE NOT NULL
);

CREATE TABLE Reuniao_Ata (
    codigo INTEGER PRIMARY KEY,
    texto TEXT NOT NULL,
    assunto VARCHAR(200) NOT NULL,
    data DATE NOT NULL,
   	matriculaCoordenador VARCHAR(15) NOT NULL,
    matriculaRedator VARCHAR(15) NOT NULL,
    FOREIGN KEY (matriculaCoordenador) REFERENCES Membro_Equipe(matricula),
    FOREIGN KEY (matriculaRedator) REFERENCES Membro_Equipe(matricula)
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
    status VARCHAR(10) CHECK (status IN ('Ativo', 'Desligado')) DEFAULT 'Ativo',

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
    status VARCHAR(30) CHECK (status IN ('Ideias', 'Stand-By', 'Fazendo', 'Feito')) NOT NULL,
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
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Projeto_Extensao (
    nomeProjeto VARCHAR(100) PRIMARY KEY,
    tipo VARCHAR(100) CHECK (tipo IN ('Curso', 'Oficina', 'Evento', 'Outros')) NOT NULL,

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto(nomeProjeto)
        ON UPDATE CASCADE
        ON DELETE CASCADE
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
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Evento (
    nomeProjeto VARCHAR(100) PRIMARY KEY,
    dataEvento DATE NOT NULL,
    duracao INTEGER CHECK (duracao > 0),

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto_Extensao(nomeProjeto)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Projeto_Ensino (
    nomeProjeto VARCHAR(100) PRIMARY KEY,
    topico VARCHAR(100) NOT NULL,

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto(nomeProjeto)
        ON UPDATE CASCADE
        ON DELETE CASCADE
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
        REFERENCES Projeto_Ensino(nomeProjeto)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (matriculaAluno)
        REFERENCES Aluno(matriculaAluno)
);

CREATE TABLE Projeto_Pesquisa (
    nomeProjeto VARCHAR(100) PRIMARY KEY,
    area VARCHAR(100) NOT NULL,

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto(nomeProjeto)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Artigo_Cientifico (
    codigoArtigo INTEGER PRIMARY KEY,
    congresso VARCHAR(100) NOT NULL,
    titulo VARCHAR(200),
    matriculaAutor VARCHAR(15),
    status VARCHAR(30) CHECK (status IN ('Submetido', 'Aceito', 'Rejeitado', 'Publicado')),

    FOREIGN KEY (matriculaAutor)
        REFERENCES Petiano(matricula)
);

CREATE TABLE Projeto_Artigo (
    nomeProjeto VARCHAR(100),
    codigoArtigo INTEGER,

    PRIMARY KEY (nomeProjeto, codigoArtigo),

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto_Pesquisa(nomeProjeto)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (codigoArtigo)
        REFERENCES Artigo_Cientifico(codigoArtigo)
);

CREATE TABLE Historico (
    semestreRef VARCHAR(10),
    matricula VARCHAR(15),
    reprovacoes INTEGER NOT NULL,

    PRIMARY KEY (semestreRef, matricula),

    FOREIGN KEY (matricula)
        REFERENCES Petiano(matricula)
);

CREATE TABLE Projeto_Petiano (
    nomeProjeto VARCHAR(100),
    matricula VARCHAR(15),

    PRIMARY KEY (nomeProjeto, matricula),

    FOREIGN KEY (nomeProjeto)
        REFERENCES Projeto(nomeProjeto)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (matricula)
        REFERENCES Petiano(matricula)
);

-- Triggers

CREATE OR REPLACE FUNCTION verificar_reprovacoes()
RETURNS TRIGGER AS $$
DECLARE
    total_reprovacoes INTEGER;
BEGIN
    SELECT SUM(reprovacoes) INTO total_reprovacoes FROM Historico WHERE matricula = NEW.matricula;

    IF total_reprovacoes >= 2 THEN
        UPDATE Petiano
        SET status = 'Desligado'
        WHERE matricula = NEW.matricula;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_reprovacoes
AFTER INSERT OR UPDATE ON Historico
FOR EACH ROW
EXECUTE FUNCTION verificar_reprovacoes();

-- Preenchimento de dados nas tabelas


INSERT INTO Membro_Equipe VALUES
('25200001', 'Anthony Barros', '2026-06-01'),
('26100001', 'Antonio Ferri', '2026-06-01'),
('23200001', 'Diogo Kruger', '2025-05-07'),
('23100001', 'Eduarda Medeiros', '2024-05-09'),
('23200002', 'João Lago', '2025-03-31'),
('1648524', 'Leomar Júnior', '2025-04-30'),
('24100001', 'Lucas Lemes', '2025-05-08'),
('24100002', 'Maria Lima', '2025-12-24'),
('24200002', 'Pablo Vicondo', '2026-06-01'),
('24200003', 'Pedro Freitas', '2025-12-24'),
('25100001', 'Ulisses Júnior', '2026-06-01'),
('22200001', 'Victor Gama', '2024-05-09'),
('24200001', 'Vinicius Lameirão', '2025-03-31');

INSERT INTO Petiano VALUES
('25200001', 'Ciência da Computacao', '2'),
('26100001', 'Ciência da Computacao', '1'),
('23200001', 'Ciência da Computacao', '6'),
('23100001', 'Ciência da Computacao', '7'),
('23200002', 'Ciência da Computacao', '6'),
('24100001', 'Engenharia de Computacao','6'),
('24100002', 'Engenharia de Computacao','6'),
('24200002', 'Ciência da Computacao', '4'),
('24200003', 'Ciência da Computacao', '4'),
('25100001', 'Ciência da Computacao', '3'),
('22200001', 'Ciência da Computacao', '7'),
('24200001', 'Ciência da Computacao', '4');

INSERT INTO Tutor VALUES
('1648524', '2031-04-30');

INSERT INTO Projeto VALUES
('SACOMP 26', '23100001', 'Semana Acadêmica da Computação de 2026', 'Feito', '1280'),
('Recepção dos Ingressantes', '23200001', 'Acolhimento dos ingressantes dos cursos de Ciência e Engenharia de Computação.', 'Stand-By', '9381'),
('Site do PET', '24200001', 'Desenvolvimento do novo site do PET Computação', 'Fazendo', '2403'),
('Eletrônica/All', '23200002', 'Realização de oficinas de eletrônica básica em escolas públicas.','Stand-By', '5505'),
('Instagram', '23100001', 'Atualização das redes do PET e da Computação UFPel.', 'Fazendo', '3043'),
('Curso UNAPI', '24200003', 'Curso de inclusão digital para idosos.', 'Stand-By', '6049'),
('Estatísticas', '22200001', 'Análise do desempenho e da evasão dos alunos de Computação.', 'Stand-By', '6723'),
('Curso Diversidade', '25100001', 'Curso de inclusão digital para alunos da UFPel.', 'Ideias', '9285'),
('Atualidades da Comp', '23200001', 'Vídeos sobre as novidades do mundo da Computação.', 'Fazendo', '1223'),
('M3CKA', '24100001', 'Desenvolvimento de atividades de robótica.', 'Fazendo', '9535'),
('Além de Ada', '24100002', 'Oficinas em escolas públicas apresentando mulheres protagonistas na Computação.', 'Fazendo', '2023'),
('Criptoanálise', '25200001', 'Métodos biométricos como ferramenta de autenticação diante da evolução da criptoanálise', 'Ideias', '9139'),
('TutorIA', '26100001', 'Desenvolvimento de uma LLM que fornece tutoria especializada aos alunos de Computação.', 'Ideias', '7089'),
('SIIEPE 2026', '23100001', 'Semana Integrada de Inovação, Ensino, Pesquisa e Extensão da UFPel de 2026', 'Stand-By', '0340'),
('Wiki Computação', '24200002','Desenvolvimento de uma página dedicada à materiais de apoio para as disciplinas de Computação', 'Ideias', '6688');

INSERT INTO Projeto_Ensino VALUES
('Recepção dos Ingressantes', 'Acolhimento'),
('Site do PET', 'Informativo'),
('Instagram', 'Informativo'),
('Atualidades da Comp', 'Informativo'),
('Curso Diversidade', 'Inclusão digital'),
('Wiki Computação', 'Informativo');

INSERT INTO Projeto_Extensao VALUES
('SACOMP 26', 'Evento'),
('Eletrônica/All', 'Oficina'),
('Curso UNAPI', 'Curso'),
('Além de Ada','Oficina'),
('SIIEPE 2026', 'Evento');

INSERT INTO Projeto_Pesquisa VALUES
('Estatísticas', 'Ciência de dados'),
('M3CKA', 'Robótica'),
('Criptoanálise', 'Segurança digital'),
('TutorIA', 'Inteligência artificial');

INSERT INTO Projeto_Petiano VALUES
('SACOMP 26', '22200001'),
('Recepção dos Ingressantes','23200002'),
('Recepção dos Ingressantes','23100001'),
('Recepção dos Ingressantes','24100002'),
('Recepção dos Ingressantes','24200003'),
('Site do PET','24200002'),
('Eletrônica/All', '23100001'),
('Eletrônica/All', '22200001'),
('Instagram', '22200001'),
('Curso UNAPI', '25100001'),
('Curso UNAPI', '26100001'),
('M3CKA', '25200001'),
('M3CKA', '24200001'),
('Curso Diversidade','25100001'),
('Curso Diversidade','24200002'),
('Além de Ada','23100001'),
('SIIEPE 2026','25200001'),
('SIIEPE 2026','26100001'),
('SIIEPE 2026','23200001'),
('SIIEPE 2026','23100001'),
('SIIEPE 2026','23200002'),
('SIIEPE 2026','24100001'),
('SIIEPE 2026','24100002'),
('SIIEPE 2026','24200002'),
('SIIEPE 2026','24200003'),
('SIIEPE 2026','25100001'),
('SIIEPE 2026','22200001'),
('SIIEPE 2026','24200001'),
('Wiki Computação','23200001');

INSERT INTO Evento VALUES
('SACOMP 26', '2026-06-22', 40),
('SIIEPE 2026', '2026-11-05', 40);

INSERT INTO Artigo_Cientifico VALUES
(101, 'WEI', 'TutorIA: Um chatbot educacional para discentes de Computação', '26100001', 'Aceito'),
(102, 'WEI', 'Métodos biométricos como ferramenta de autenticação diante da evolução da criptoanálise', '25200001', 'Aceito'),
(103, 'WEI', 'Aplicações de robótica no ensino fundamental: Relato de experiência', '24100001', 'Aceito'),
(104, 'SulPET', 'Análise da evasão discente nos cursos de Computação da UFPel utilizando técnicas de mineração de dados', '22200001', 'Submetido');

INSERT INTO Projeto_Artigo VALUES
('TutorIA', 101),
('Criptoanálise', 102),
('M3CKA', 103),
('Estatísticas', 104);

INSERT INTO Reuniao_Ata VALUES
(1565, 'Falas e decisões.', 'Discussao sobre andamento dos projetos.', '2026-03-10', '26100001', '23200001'),
(2425, 'Definição de data, local e atividades.', 'Planejamento do evento.', '2026-04-02', '23200002', '23100001'); 

INSERT INTO Reuniao_Membro VALUES
(1565, '23100001'),
(1565, '22200001'),
(2425, '23200002'),
(2425, '24100002');

INSERT INTO Reuniao_Projeto VALUES
(1565, 'Eletrônica/All'),
(1565, 'Curso UNAPI'),
(1565, 'Recepção dos Ingressantes'),
(2425, 'SACOMP 26');

INSERT INTO Membro_Externo VALUES
('Escola Municipal Pelotas', 'Rua Central 100', 'Alunos do ensino fundamental', 'Mariana Costa', '(53)99999-1111'),
('IFSul', 'Av. Bento 500', 'Estudantes de tecnologia', 'Ricardo Alves', '(53)99999-2222');

INSERT INTO MembroExterno_ProjetoExtensao VALUES
('Escola Municipal Pelotas', 'Eletrônica/All'),
('IFSul', 'SACOMP 26');

INSERT INTO Aluno VALUES
('25685742', 'Ciencia da Computacao'),
('24206174', 'Ciencia da Computacao'),
('17634578', 'Engenharia da Computacao');

INSERT INTO Projeto_Aluno VALUES
('Recepção dos Ingressantes', '25685742'),
('Recepção dos Ingressantes', '24206174'),
('Curso Diversidade', '17634578');

INSERT INTO Historico VALUES
('2026/1', '23100001', 0),
('2026/1', '23200002', 0),
('2026/1', '24100002', 1),
('2026/1', '24200003', 1);

