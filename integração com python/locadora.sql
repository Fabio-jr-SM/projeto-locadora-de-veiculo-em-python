CREATE table carros(
	id_carro INTEGER unique PRIMARY KEY AUTOINCREMENT,
	marca TEXT,
	modelo TEXT,
	cor TEXT,
	quantidade INTEGER,
	ano INTEGER,
	preco_dia INTEGER
);

CREATE table pessoa(
	id_pessoa INTEGER unique PRIMARY KEY AUTOINCREMENT,
	nome TEXT,
	idade INTEGER,
	cpf INTEGER,
	cnh INTEGER
);

CREATE table aluga(
	id_aluguel INTEGER unique PRIMARY KEY AUTOINCREMENT,
	data_alugada TEXT,
	data_devoluçao TEXT,
	preco_aluguel INTEGER,
	id_carro INTEGER,
	id_pessoa INTEGER,
	FOREIGN key(id_pessoa) REFERENCES pessoa(id_pessoa),
	FOREIGN key(id_carro) REFERENCES carros(id_carro)
);

insert into carros (marca, modelo, ano, cor, preco_dia, quantidade)
	VALUES("Toyota", "Camry", 2022, "Prata", 80.0, 2),
		("Honda", "Civic", 2021, "Azul", 95.0, 1),
		("Ford", "Escape", 2023, "Preto", 90.0, 5),
		("Chevrolet", "Trax", 2022, "Branco", 85.0, 7),
		("Nissan", "Versa", 2021, "Vermelho", 70.0,  4),
		("Hyundai", "Accent", 2022, "Prata", 65.0,  7),
		("Renault", "Kwid", 2017, "Prata", 50.0,  2),
		("Volkswagen", "Golf", 2023, "Azul", 88.0, 3),
		("Mazda", "Mazda3", 2022, "Cinza", 75.0,  3),
		("Kia", "Forte", 2023, "Vermelho", 82.0,  5);
		
select *from carros;

insert into pessoa (nome, idade, cpf, cnh)
	VALUES("Maria", 22 , 01802625900 , 11557786927),
		("João", 30, 12345678901, 9876543210),
		("Ana", 25, 98765432109, 9988776655),
		("Carlos", 28, 11223344556, 5544332211),
		("Larissa", 35, 87654321098, 1122334455),
		("Pedro", 40, 55544433322, 9998887776),
		("Isabel", 27, 99988877766, 2233445566),
		("Rafael", 33, 65432109876, 777888999),
		("Camila", 29, 32109876543, 4445556667),
		("Gabriel", 22 , 08792569348 , 08970059011);

SELECT * from pessoa;

INSERT into aluga(data_alugada, data_devoluçao, preco_aluguel, id_carro, id_pessoa)
	VALUES("05/12/2023", "15/12/2023", 800.0, 1 , 1),
			("10/12/2023", "20/12/2023", 950.0, 2, 2),
			("08/12/2023", "18/12/2023", 900.0, 3, 3),
			("12/12/2023", "22/12/2023", 850.0, 4, 4),
			("07/12/2023", "17/12/2023", 700.0, 5, 5),
			("06/12/2023", "16/12/2023", 650.0, 6, 6),
			("09/12/2023", "19/12/2023", 500.0, 7, 7),
			("11/12/2023", "21/12/2023", 880.0, 8, 8),
			("13/12/2023", "23/12/2023", 750.0, 9, 9),
			("14/12/2023", "24/12/2023", 820.0, 10, 10);

SELECT *from aluga;


--Relatório da Locação do carro
select pessoa.nome, pessoa.cpf, pessoa.cnh, carros.modelo, aluga.data_alugada, aluga.data_devoluçao, aluga.preco_aluguel

FROM  aluga 
JOIN pessoa on aluga.id_pessoa = pessoa.id_pessoa
JOIN carros on aluga.id_carro = carros.id_carro;
