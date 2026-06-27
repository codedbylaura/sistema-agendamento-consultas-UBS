-- ============================================================
-- SISTEMA DE AGENDAMENTO DE CONSULTAS - UBS
-- Banco de Dados PostgreSQL
-- ============================================================

-- Extensão para geração de UUIDs (opcional, mas útil)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";


-- ============================================================
-- TABELA: endereco
-- Reutilizada por pacientes e profissionais
-- ============================================================
CREATE TABLE endereco (
    id          SERIAL PRIMARY KEY,
    logradouro  VARCHAR(150) NOT NULL,
    numero      VARCHAR(10)  NOT NULL,
    complemento VARCHAR(100),
    bairro      VARCHAR(100) NOT NULL,
    cidade      VARCHAR(100) NOT NULL,
    estado      CHAR(2)      NOT NULL,
    cep         CHAR(8)      NOT NULL,
    criado_em   TIMESTAMP    NOT NULL DEFAULT NOW()
);


-- ============================================================
-- TABELA: paciente
-- ============================================================
CREATE TABLE paciente (
    id              SERIAL PRIMARY KEY,
    nome            VARCHAR(150)        NOT NULL,
    cpf             CHAR(11)            NOT NULL UNIQUE,
    data_nascimento DATE                NOT NULL,
    sexo            CHAR(1)             NOT NULL CHECK (sexo IN ('M', 'F', 'O')),
    telefone        VARCHAR(15),
    email           VARCHAR(150)        UNIQUE,
    cartao_sus      VARCHAR(15)         UNIQUE,
    endereco_id     INT                 REFERENCES endereco(id) ON DELETE SET NULL,
    ativo           BOOLEAN             NOT NULL DEFAULT TRUE,
    criado_em       TIMESTAMP           NOT NULL DEFAULT NOW(),
    atualizado_em   TIMESTAMP           NOT NULL DEFAULT NOW()
);

COMMENT ON COLUMN paciente.sexo IS 'M = Masculino, F = Feminino, O = Outro';
COMMENT ON COLUMN paciente.cartao_sus IS 'Número do Cartão Nacional de Saúde (CNS)';


-- ============================================================
-- TABELA: especialidade
-- Ex: Clínica Geral, Pediatria, Enfermagem, Odontologia
-- ============================================================
CREATE TABLE especialidade (
    id        SERIAL PRIMARY KEY,
    nome      VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT
);


-- ============================================================
-- TABELA: profissional_saude
-- ============================================================
CREATE TABLE profissional_saude (
    id               SERIAL PRIMARY KEY,
    nome             VARCHAR(150)  NOT NULL,
    cpf              CHAR(11)      NOT NULL UNIQUE,
    registro_conselho VARCHAR(20)  NOT NULL UNIQUE,   -- CRM, COREN, CRO etc.
    tipo_conselho    VARCHAR(10)   NOT NULL,           -- CRM, COREN, CRO...
    especialidade_id INT           NOT NULL REFERENCES especialidade(id),
    telefone         VARCHAR(15),
    email            VARCHAR(150)  UNIQUE,
    endereco_id      INT           REFERENCES endereco(id) ON DELETE SET NULL,
    ativo            BOOLEAN       NOT NULL DEFAULT TRUE,
    criado_em        TIMESTAMP     NOT NULL DEFAULT NOW(),
    atualizado_em    TIMESTAMP     NOT NULL DEFAULT NOW()
);

COMMENT ON COLUMN profissional_saude.registro_conselho IS 'Número do registro no conselho de classe (CRM, COREN, CRO...)';


-- ============================================================
-- TABELA: horario_disponivel
-- Define os horários de atendimento de cada profissional
-- ============================================================
CREATE TABLE horario_disponivel (
    id               SERIAL PRIMARY KEY,
    profissional_id  INT     NOT NULL REFERENCES profissional_saude(id) ON DELETE CASCADE,
    dia_semana       SMALLINT NOT NULL CHECK (dia_semana BETWEEN 0 AND 6),  -- 0=Dom, 6=Sáb
    hora_inicio      TIME    NOT NULL,
    hora_fim         TIME    NOT NULL,
    duracao_consulta SMALLINT NOT NULL DEFAULT 30,   -- duração em minutos
    ativo            BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_horario CHECK (hora_fim > hora_inicio)
);

COMMENT ON COLUMN horario_disponivel.dia_semana IS '0=Domingo, 1=Segunda, 2=Terça, 3=Quarta, 4=Quinta, 5=Sexta, 6=Sábado';
COMMENT ON COLUMN horario_disponivel.duracao_consulta IS 'Duração padrão de cada consulta em minutos';


-- ============================================================
-- TABELA: consulta
-- Núcleo do sistema de agendamento
-- ============================================================
CREATE TABLE consulta (
    id               SERIAL PRIMARY KEY,
    paciente_id      INT          NOT NULL REFERENCES paciente(id),
    profissional_id  INT          NOT NULL REFERENCES profissional_saude(id),
    data_hora        TIMESTAMP    NOT NULL,
    duracao_min      SMALLINT     NOT NULL DEFAULT 30,
    status           VARCHAR(20)  NOT NULL DEFAULT 'agendada'
                        CHECK (status IN ('agendada', 'confirmada', 'realizada', 'cancelada', 'falta')),
    motivo           TEXT,                          -- motivo da consulta informado pelo paciente
    observacoes      TEXT,                          -- observações do profissional
    cancelado_por    VARCHAR(20)  CHECK (cancelado_por IN ('paciente', 'profissional', 'unidade')),
    motivo_cancelamento TEXT,
    criado_em        TIMESTAMP    NOT NULL DEFAULT NOW(),
    atualizado_em    TIMESTAMP    NOT NULL DEFAULT NOW(),

    -- Impede dois agendamentos do mesmo profissional no mesmo horário
    CONSTRAINT uq_profissional_horario UNIQUE (profissional_id, data_hora)
);

COMMENT ON COLUMN consulta.status IS
    'agendada=marcada, confirmada=paciente confirmou, realizada=atendido, cancelada=cancelado, falta=não compareceu';


-- ============================================================
-- TABELA: historico_status_consulta
-- Rastreia todas as mudanças de status de uma consulta
-- ============================================================
CREATE TABLE historico_status_consulta (
    id          SERIAL PRIMARY KEY,
    consulta_id INT          NOT NULL REFERENCES consulta(id) ON DELETE CASCADE,
    status_ant  VARCHAR(20),
    status_novo VARCHAR(20)  NOT NULL,
    alterado_em TIMESTAMP    NOT NULL DEFAULT NOW(),
    alterado_por VARCHAR(100)               -- usuário ou sistema que fez a alteração
);


-- ============================================================
-- ÍNDICES — Melhoram a performance das buscas mais comuns
-- ============================================================

-- Busca de paciente por CPF e nome
CREATE INDEX idx_paciente_cpf   ON paciente(cpf);
CREATE INDEX idx_paciente_nome  ON paciente(nome);

-- Busca de consultas por paciente, profissional e data
CREATE INDEX idx_consulta_paciente     ON consulta(paciente_id);
CREATE INDEX idx_consulta_profissional ON consulta(profissional_id);
CREATE INDEX idx_consulta_data_hora    ON consulta(data_hora);
CREATE INDEX idx_consulta_status       ON consulta(status);

-- Busca de horários por profissional
CREATE INDEX idx_horario_profissional ON horario_disponivel(profissional_id);


-- ============================================================
-- FUNÇÃO + TRIGGER — Atualiza "atualizado_em" automaticamente
-- ============================================================
CREATE OR REPLACE FUNCTION fn_atualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_paciente_atualizado
    BEFORE UPDATE ON paciente
    FOR EACH ROW EXECUTE FUNCTION fn_atualizar_timestamp();

CREATE TRIGGER trg_profissional_atualizado
    BEFORE UPDATE ON profissional_saude
    FOR EACH ROW EXECUTE FUNCTION fn_atualizar_timestamp();

CREATE TRIGGER trg_consulta_atualizado
    BEFORE UPDATE ON consulta
    FOR EACH ROW EXECUTE FUNCTION fn_atualizar_timestamp();


-- ============================================================
-- FUNÇÃO + TRIGGER — Registra histórico ao mudar status da consulta
-- ============================================================
CREATE OR REPLACE FUNCTION fn_registrar_historico_status()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO historico_status_consulta (consulta_id, status_ant, status_novo)
        VALUES (NEW.id, OLD.status, NEW.status);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_historico_status
    AFTER UPDATE ON consulta
    FOR EACH ROW EXECUTE FUNCTION fn_registrar_historico_status();


-- ============================================================
-- DADOS INICIAIS (SEEDS)
-- ============================================================

-- Especialidades comuns em UBS
INSERT INTO especialidade (nome, descricao) VALUES
    ('Clínica Geral',   'Atendimento médico geral para adultos'),
    ('Pediatria',        'Atendimento médico para crianças e adolescentes'),
    ('Enfermagem',       'Atendimento e procedimentos de enfermagem'),
    ('Odontologia',      'Atendimento odontológico básico'),
    ('Ginecologia',      'Saúde da mulher'),
    ('Nutrição',         'Orientação nutricional'),
    ('Psicologia',       'Saúde mental e acompanhamento psicológico');


-- ============================================================
-- EXEMPLOS DE USO (comentados — rode só para testes)
-- ============================================================

/*
-- Inserir um endereço
INSERT INTO endereco (logradouro, numero, bairro, cidade, estado, cep)
VALUES ('Rua das Flores', '123', 'Centro', 'São Paulo', 'SP', '01310100');

-- Inserir um paciente
INSERT INTO paciente (nome, cpf, data_nascimento, sexo, telefone, email, endereco_id)
VALUES ('Maria da Silva', '12345678901', '1990-05-15', 'F', '11999990000', 'maria@email.com', 1);

-- Inserir um profissional
INSERT INTO profissional_saude (nome, cpf, registro_conselho, tipo_conselho, especialidade_id, email)
VALUES ('Dr. João Souza', '98765432100', '123456', 'CRM', 1, 'dr.joao@ubs.gov.br');

-- Definir horário de atendimento (segunda a sexta, 8h às 12h, consultas de 30min)
INSERT INTO horario_disponivel (profissional_id, dia_semana, hora_inicio, hora_fim, duracao_consulta)
VALUES (1, 1, '08:00', '12:00', 30),
       (1, 2, '08:00', '12:00', 30),
       (1, 3, '08:00', '12:00', 30),
       (1, 4, '08:00', '12:00', 30),
       (1, 5, '08:00', '12:00', 30);

-- Agendar uma consulta
INSERT INTO consulta (paciente_id, profissional_id, data_hora, motivo)
VALUES (1, 1, '2026-07-01 08:00:00', 'Dor de cabeça frequente');

-- Confirmar consulta
UPDATE consulta SET status = 'confirmada' WHERE id = 1;

-- Cancelar consulta
UPDATE consulta
SET status = 'cancelada', cancelado_por = 'paciente', motivo_cancelamento = 'Viagem'
WHERE id = 1;
*/