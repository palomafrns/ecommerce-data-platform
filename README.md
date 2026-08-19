E-commerce Data Platform

Pipeline de engenharia de dados para ingestão, processamento e carga de dados de e-commerce (produtos), construído em Python com PostgreSQL como banco de destino.

📋 Sobre o projeto

Este projeto implementa um pipeline ETL que extrai dados brutos de produtos (formato JSON), processa e organiza essas informações em camadas de staging, e realiza a carga estruturada em um banco de dados PostgreSQL usando psycopg2.

O objetivo é praticar e demonstrar conceitos de engenharia de dados: modelagem, staging, validação de qualidade de dados e ETL multi-tabela.

🏗️ Arquitetura
data/
├── raw/
│   └── products/          # Dados brutos extraídos (JSON)
└── staging/
    └── products/
        ├── dimensions.json
        ├── images.json
        └── metadata.json

O fluxo segue o padrão:

Raw → Staging → Banco de dados (PostgreSQL)

Raw: dados brutos de produtos são armazenados como JSON, sem transformação
Staging: os dados são separados e organizados em arquivos intermediários por domínio (dimensões, imagens, metadados)
Load: os dados de staging são carregados no PostgreSQL através de scripts Python com psycopg2, respeitando o mapeamento entre campos de origem e colunas do banco
🛠️ Tecnologias utilizadas
Python — linguagem principal do pipeline
psycopg2 — conexão e carga de dados no PostgreSQL
PostgreSQL — banco de dados relacional de destino
Docker Compose — orquestração do ambiente de banco de dados
pandas / numpy — manipulação e transformação de dados