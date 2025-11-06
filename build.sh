#!/bin/bash

# 1. Instala as dependências
echo ">>> PASSO 1: Instalando dependências..."
pip install -r requirements.txt

# 2. Roda as migrações do banco de dados
echo ">>> PASSO 2: Rodando migrações do banco (db upgrade)..."
flask db upgrade

# 3. Roda o script de seed
echo ">>> PASSO 3: Populando o banco (seed)..."
python seed.py

echo ">>> BUILD CONCLUÍDO!"