-- Restaurante Sabor & Arte — executado por banco-dados/criar_banco.py ou setup.bat
CREATE DATABASE IF NOT EXISTS restaurante
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE restaurante;

CREATE TABLE IF NOT EXISTS prato (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(150) NOT NULL,
  categoria VARCHAR(50) NOT NULL COMMENT 'Entrada, Prato principal, Sobremesa, Bebida',
  descricao TEXT DEFAULT NULL,
  preco DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB;
