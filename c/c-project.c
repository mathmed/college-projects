#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <locale.h>
#include <time.h>
#include <unistd.h>


typedef struct ingredientes{
	char nome[81], medida[81];
  	int quantidade;
	float valor, valor_venda, medida_a_ser_vendida;
	int codigo_ingrediente;
  	struct ingredientes* prox;
}Ingredientes;

typedef struct caixa{
	char tipo[81], data[81], nome_relatorio[81];
	float valorTransicao;
	int dia, mes, ano;
	struct caixa* prox;
}Caixa;


Ingredientes* _cria(void);
Caixa* __cria(void);
void _pedidos(Ingredientes** ing, Caixa** caixa);
void _relatorios(Ingredientes* ing, Caixa* caixa);
void _estoque(Ingredientes** ing, Caixa** caixa);
void _verEstoque(Ingredientes* ing);
void _verEstoqueCodigo(Ingredientes* ing, int escolha);
void _verEstoqueNome(Ingredientes* ing, int escolha);
void _verEstoquePrecoDeCompra(Ingredientes* ing, int escolha);
void _verEstoquePrecoDeVenda(Ingredientes* ing, int escolha);
void _verEstoqueQuantidadeArmazenado(Ingredientes* ing, int escolha);
void _verEstoqueCompleto(Ingredientes* ing, int escolha);
int _verificaUltimoCodigo(Ingredientes* ing);

void _insere(Ingredientes** ing, Caixa** caixa);
void _insereNovo(Ingredientes** ing, Caixa** caixa);
void _insereExistente(Ingredientes** ing, Caixa** caixa);

void _alteraPrecos(Ingredientes** ing);
void _removeEstoque(Ingredientes** ing);
int _inEstoque(Ingredientes* ing,int aux);
int dataAComparar (Caixa* p);
int dataSistema();
int validaData(char *data1, char *data2, int *dataAComparar1, int *dataAComparar2);
void _relatorioTudo(Ingredientes* ing, Caixa* caixa, int opcao);
void _relatorioDiario(Ingredientes* ing, Caixa* caixa, int opcao);
void _relatorioSemanal(Ingredientes* ing, Caixa* caixa, int opcao);
void _relatorioMensal(Ingredientes* ing, Caixa* caixa, int opcao);
void _relatorioSemestral(Ingredientes* ing, Caixa* caixa, int opcao);
void _relatorioAnual(Ingredientes* ing, Caixa* caixa, int opcao);
void _relatorioPersonalizado(Ingredientes* ing, Caixa* caixa, int opcao);

void informacoes(void);

int main(void)
{
    setlocale(LC_ALL, "Portuguese");
	Ingredientes* ing;
	Caixa* caixa;
	ing = _cria();
	caixa = __cria();
	int op = 0, opcao1;
	char opcao[10];



	while(op != 99){
	system("cls");
	printf("\n\t*************************************************************************\n");
	printf("\t* _               _   _  _____ _    _  ____   _   _ ______ _______ \t*\n");
	printf("\t* | |        /\\   | \\ | |/ ____| |  | |/ __ \\ | \\ | |  ____|__   __| \t*\n");
	printf("\t* | |       /  \\  |  \\| | |    | |__| | |  | ||  \\| | |__     | | \t*\n"   );
	printf("\t* | |      / /\\ \\ | . ` | |    |  __  | |  | || . ` |  __|    | | \t*\n" );
	printf("\t* | |____ / ____ \\| |\\  | |____| |  | | |__| || |\\  | |____   | | \t*\n" );
	printf("\t* |______/_/    \\_\\_| \\_|\\_____|_|  |_|\\____(_)_| \\_|______|  |_| \t*\n"   );
	printf("\n\t*************************************************************************\n");


	printf("\n\n\t\t[1] - Pedidos \n\t\t[2] - Opções de Estoque \n\t\t[3] - Relatórios \n\t\t[4] - Informações do Software \n\t\t[9] - Sair\n \t\t"); //escolher as opções do sistema
	printf("\n\t\tEscolha:");
	scanf("%s", opcao);
	opcao1= atoi(opcao);

	switch(opcao1){ //saber qual função chamar

		case 1:
			_pedidos(&ing, &caixa);
			break;
		case 2:
      		_estoque(&ing, &caixa);
			break;
		case 3:
			_relatorios(ing, caixa);
			break;
		case 4:
			informacoes();
			break;
		case 9:
			exit(1);
		default:
			printf("\nOpcão inválida! \n\n");
			break;

		}

	}
	return 0;
}

Ingredientes* _cria(void){
  return NULL;

}                     //função para deixar o vetor NULL

Caixa* __cria(void){
  return NULL;

}                     //função para deixar o vetor NULL


void _pedidos(Ingredientes** ing, Caixa** caixa) {     //função pedidos
	system("cls");
	struct tm *info;
	time_t segundos;
	Ingredientes* p;
	int aux;
	char ver_novamente, aux2[10];
	float valorPedido;
	printf("\n\t\t\t  _____  ______ _____ _____ _____   ____   _____ ");
	printf("\n\t\t\t |  __ \\|  ____|  __ \\_   _|  __ \\ / __ \\ / ____|");
	printf("\n\t\t\t | |__) | |__  | |  | || | | |  | | |  | | (___  ");
	printf("\n\t\t\t |  ___/|  __| | |  | || | | |  | | |  | |\\___ \\ ");
	printf("\n\t\t\t | |    | |____| |__| || |_| |__| | |__| |____) |");
	printf("\n\t\t\t |_|    |______|_____/_____|_____/ \\____/|_____/ ");

	printf("\n\n\t\t\t***************************************************");
    printf("\n\t\t\t*                                                 *");
    printf("\n\t\t\t*      		ESCOLHA OS INGREDIENTES 	  *");
    printf("\n\t\t\t*                                                 *");
    printf("\n\t\t\t***************************************************\n\n");
	if(*ing != NULL){

		for(p = *ing;p != NULL;p =p->prox){
			if(p->quantidade > 0){
					printf("%s: ", p->nome);
					printf("\nValor de %5.2f %s: R$%5.2f", p->medida_a_ser_vendida, p->medida, p->valor_venda);
					printf("\nInforme a quantidade de porções de %5.2f %s: ", p->medida_a_ser_vendida, p->medida);
					scanf("%s", aux2);
					aux = atoi(aux2);
					printf("\n\n");
					if(p->quantidade >= (aux*p->medida_a_ser_vendida) && aux > 0){
						p->quantidade -= (aux*p->medida_a_ser_vendida);
						valorPedido += (p->valor_venda*aux);
						Caixa* cnovo = (Caixa*)malloc(sizeof(Caixa));
						cnovo->valorTransicao=valorPedido;
						char _tipo[] = "Entrada";
						strcpy(cnovo->tipo, _tipo);
						strcpy(cnovo->nome_relatorio, p->nome);

						time(&segundos); // guardando segundos
						info = localtime(&segundos); //guardando em info
						strftime(cnovo->data, 80, "%d/%m/%Y ás %X", info); //guardando em data
						cnovo->dia = info->tm_mday;
						cnovo->mes = info->tm_mon;
						cnovo->ano = info->tm_year;
						cnovo->prox = *caixa;
						*caixa = cnovo;

					}else{
						printf("\nVocê digitou um valor inválido. Informe uma quantidade igual ou inferior à %d %s:\n\n", p->quantidade, p->medida);
						scanf("%s", aux2);
						aux = atoi(aux2);
						if(p->quantidade >= (aux*p->medida_a_ser_vendida) && aux > 0){
							p->quantidade -= (aux*p->medida_a_ser_vendida);
							valorPedido += (p->valor_venda*aux);
							Caixa* cnovo = (Caixa*)malloc(sizeof(Caixa));
							cnovo->valorTransicao=valorPedido;

							char _tipo[] = "Entrada";
							strcpy(cnovo->tipo, _tipo);
							strcpy(cnovo->nome_relatorio, p->nome);

							time(&segundos); // guardando segundos
							info = localtime(&segundos); //guardando em info
							strftime(cnovo->data, 80, "%d/%m/%Y ás %X", info); //guardando em data
							cnovo->dia = info->tm_mday;
							cnovo->mes = info->tm_mon;
							cnovo->ano = info->tm_year;

							cnovo->prox = *caixa;
							*caixa = cnovo;
						}
			}
		}

		}
		printf("O valor de seu pedido é: R$%5.2f\n\n", valorPedido);
		printf("\n\nDigite S para fazer um novo pedido ou outra tecla para retornar ao menu inicial:");
		scanf("%s", &ver_novamente);
		if(ver_novamente == 'S'){
			_pedidos(ing, caixa);
		}
	}else{
		printf("Não existe produtos no estoque para realizar pedidos, adicione e tente novamente. Digite S para retornar ao menu:");
		scanf("%s", &ver_novamente);

	}
}

void _estoque(Ingredientes** ing, Caixa** caixa){
	system("cls");
	char option[10];
	int option1;
	printf("\n\t\t\t  ______  _____ _______ ____   ____  _    _ ______   ");
	printf("\n\t\t\t |  ____|/ ____|__   __/ __ \\ / __ \\| |  | |  ____|");
	printf("\n\t\t\t | |__  | (___    | | | |  | | |  | | |  | | |__     ");
	printf("\n\t\t\t |  __|  \\___ \\   | | | |  | | |  | | |  | |  __|  ");
	printf("\n\t\t\t | |____ ____) |  | | | |__| | |__| | |__| | |____   ");
	printf("\n\t\t\t |______|_____/   |_|  \\____/ \\___\\_ \\____/|______|");


	printf("\n\n\n\n\t\t[1] - Ver Estoque\n\t\t[2] - Adicionar Ingrediente\n\t\t[3] - Alterar Preços\n\t\t[4] - Remover do Estoque \n\t\t");
	printf("\n\n\n\t\tEscolha:");
	scanf("%s", option);
	option1 = atoi(option);
	switch (option1) {
		case 1:
			_verEstoque(*ing);
			break;
		case 2:
			_insere(ing, caixa);
			break;
		case 3:
			_alteraPrecos(ing);
			break;
		case 4:
			_removeEstoque(ing);
			break;
		case 0:
			printf("\n\t\tOpção inválida! Retornando ao menu...\n\n");
			sleep(3);
			break;

		}


}

void _verEstoque(Ingredientes* ing){
	system("cls");
	char escolha[10], escolha2[10];
	int escolha1, escolha3;
 	printf("\n\n\t\t\t*************************************************************");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*                   VIZUALIZAR ESTOQUE                      *");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*************************************************************");
	printf("\n\n\t\tDeseja vizualizar seu estoque a partir de:\n\n");
	printf("\t\t[1] - Código\n\t\t[2] - Nome\n\t\t[3] - Preço de compra\n\t\t[4] - Preço de venda\n\t\t[5] - Quantidade armazenado\n\t\t[6] - Vizualizar tudo\n\t\t");
	printf("\n\t\tEscolha:");
	scanf("%s", escolha);
	escolha1 = atoi(escolha);
	printf("\n\n\t\tDeseja vizualizar de qual maneira:\n\n");
	printf("\t\t[1] - Forma de tabela\n\t\t[2] - Forma corrida\n\t\t");
	printf("\n\t\tEscolha:");
	scanf("%s", escolha2);
	escolha3 = atoi(escolha2);
	if(escolha3 == 1 || escolha3 == 2){

		switch(escolha1){
			case 1:
				_verEstoqueCodigo(ing, escolha3);
				break;
			case 2:
				_verEstoqueNome(ing, escolha3);
				break;
			case 3:
				_verEstoquePrecoDeCompra(ing, escolha3);
				break;
			case 4:
				_verEstoquePrecoDeVenda(ing, escolha3);
				break;
			case 5:
				_verEstoqueQuantidadeArmazenado(ing, escolha3);
				break;
			case 6:
				_verEstoqueCompleto(ing, escolha3);
				break;
			case 0:
				printf("\n\t\tVocê digitou algo inválido. Retornando ao menu... \n");
				sleep(3);
				break;
		}
	}else{
		printf("\n\nVocê digitou algo inválido. Retornando ao menu... \n");
		sleep(3);
	}
}



void _verEstoqueCodigo(Ingredientes* ing, int escolha){
	system("cls");
	char ver_novamente, codigo[10];
	Ingredientes* p;
	int codigo1, contador = 0;
	printf("\n\n\t\t\t*************************************************************");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*                 VIZUALIZAÇÃO POR CÓDIGO                *");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*************************************************************\n\n");
	printf("\n Informe o código que deseja pesquisar:");
	scanf("%s", codigo);
	codigo1 = atoi(codigo);
	if(escolha==2){
	  	for(p =ing; p != NULL; p =p->prox){
	  		if(p->codigo_ingrediente == codigo1){
    			printf("\nCódigo: %d\nNome do produto: %s\nQuantidade de %s no estoque: %d\nValor de compra a cada %5.2f %s: R$%5.2f\nValor de venda a cada %5.2f %s: R$%5.2f\n\n",
    			 p->codigo_ingrediente, p->nome, p->medida, p->quantidade, p->medida_a_ser_vendida, p->medida, p->valor, p->medida_a_ser_vendida, p->medida, p->valor_venda);
    			contador++;
    		}
	  	}
	  	if(contador == 0){
	  		 printf("\n\nCódigo de produto não encontrado. Digite S para pesquisar novamente ou outra tecla para sair:\n ");
	  		 scanf("%s", &ver_novamente);
	  		 if(ver_novamente == 'S'){
	  		 	_verEstoqueCodigo(ing, escolha);
	  		 }
	  	}else{
	  		printf("\n\nDigite S para retornar ao menu principal.\n ");
	  		scanf("%s", &ver_novamente);
	  	}
	}else{
		contador=0;
		system("cls");
		printf("[Codigo]\t\t[Nome do produto]\t\t[Quantidade no estoque]\t\t\t  [Valor de compra]\t\t\t  [Valor de venda]\n");
	  	for(p =ing; p != NULL; p =p->prox){
	  		if(p->codigo_ingrediente == codigo1){
				printf("\n%4d\t\t\t%15s\t\t\t   %5d%10s\t\t\t%5.2f%10s:R$%5.2f\t\t\t%5.2f%10s:R$%5.2f",
		    			 p->codigo_ingrediente, p->nome,  p->quantidade, p->medida, p->medida_a_ser_vendida, p->medida, p->valor, p->medida_a_ser_vendida, p->medida, p->valor_venda);

    			contador++;
    		}
	  	}
	  	if(contador == 0){
	  		 printf("\n\nCódigo de produto não encontrado. Digite S para pesquisar novamente ou outra tecla para sair:\n ");
	  		 scanf("%s", &ver_novamente);
	  		 if(ver_novamente == 'S'){
	  		 	_verEstoqueCodigo(ing, escolha);
	  		 }
	  	}else{
	  		printf("\n\nDigite S para retornar ao menu principal.\n ");
	  		scanf("%s", &ver_novamente);
	  	}

	}

}

void _verEstoqueNome(Ingredientes* ing, int escolha){
	system("cls");
	char ver_novamente, nome_ingrediente[81];
	Ingredientes* p;
	int contador;
	printf("\n\n\t\t\t*************************************************************");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*                 VIZUALIZAÇÃO POR NOME                   *");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*************************************************************\n\n");
	printf("\n Informe o nome que deseja pesquisar:");
	scanf(" %80[^\n]", &nome_ingrediente);
	if(escolha == 2){
		for(p =ing; p != NULL; p =p->prox){
			if(strcmp(nome_ingrediente, p->nome)==0){
	    		printf("\nCódigo: %d\nNome do produto: %s\nQuantidade de %s no estoque: %d\nValor de compra a cada %5.2f %s: R$%5.2f\nValor de venda a cada %5.2f %s: R$%5.2f\n\n",
	    			 p->codigo_ingrediente, p->nome, p->medida, p->quantidade, p->medida_a_ser_vendida, p->medida, p->valor, p->medida_a_ser_vendida, p->medida, p->valor_venda);
	    		contador++;
			}
		}
		if(contador == 0){
		  		 printf("\n\nNome de produto não encontrado. Digite S para pesquisar novamente ou outra tecla para sair: ");
		  		 scanf("%s", &ver_novamente);
		  		 if(ver_novamente == 'S'){
		  		 	_verEstoqueNome(ing, escolha);
		  		 }
		}else{
			printf("\n\nDigite S para retornar ao menu principal.\n ");
		  	scanf("%s", &ver_novamente);
		}

	}else{
		contador =0;
		system("cls");
		printf("[Codigo]\t\t[Nome do produto]\t\t[Quantidade no estoque]\t\t\t  [Valor de compra]\t\t\t  [Valor de venda]\n");
		for(p =ing; p != NULL; p =p->prox){
			if(strcmp(nome_ingrediente, p->nome)==0){
				printf("\n%4d\t\t\t%15s\t\t\t   %5d%10s\t\t\t%5.2f%10s:R$%5.2f\t\t\t%5.2f%10s:R$%5.2f",
		    			 p->codigo_ingrediente, p->nome,  p->quantidade, p->medida, p->medida_a_ser_vendida, p->medida, p->valor, p->medida_a_ser_vendida, p->medida, p->valor_venda);

	    		contador++;
			}
		}
		if(contador == 0){
		  		 printf("\n\nNome de produto não encontrado. Digite S para pesquisar novamente ou outra tecla para sair: ");
		  		 scanf("%s", &ver_novamente);
		  		 if(ver_novamente == 'S'){
		  		 	_verEstoqueNome(ing, escolha);
		  		 }
		}else{
			printf("\n\nDigite S para retornar ao menu principal.\n ");
		  	scanf("%s", &ver_novamente);
		}

	}

}

void _verEstoquePrecoDeCompra(Ingredientes* ing, int escolha){
	system("cls");
	char ver_novamente;
	char preco_max_ingrediente[100], preco_min_ingrediente[100];
	float preco_max_ingrediente1, preco_min_ingrediente1;
	int contador;
	Ingredientes* p;
	printf("\n\n\t\t\t*************************************************************");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*                 VIZUALIZAÇÃO POR PREÇO                 *");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*************************************************************\n\n");
	printf("\n Informe o menor preço de busca:");
	scanf("%s", preco_min_ingrediente);
	printf("\n Informe o maior preço de busca:");
	scanf("%s", preco_max_ingrediente);
	preco_min_ingrediente1 = atof(preco_min_ingrediente);
	preco_max_ingrediente1 = atof(preco_max_ingrediente);
	if(escolha==2){
		for(p =ing; p != NULL; p = p->prox){
			if(p->valor <= preco_max_ingrediente1 && p->valor >= preco_min_ingrediente1){
				printf("\nCódigo: %d\nNome do produto: %s\nQuantidade de %s no estoque: %d\nValor de compra a cada %5.2f %s: R$%5.2f\nValor de venda a cada %5.2f %s: R$%5.2f\n\n",
	    			 p->codigo_ingrediente, p->nome, p->medida, p->quantidade, p->medida_a_ser_vendida, p->medida, p->valor, p->medida_a_ser_vendida, p->medida, p->valor_venda);
	    		contador++;
			}
		}
		if(contador == 0){
		  		 printf("\n\nNenhum produto encontrado. Digite S para pesquisar novamente ou outra tecla para sair:\n ");
		  		 scanf("%s", &ver_novamente);
		  		 if(ver_novamente == 'S'){
		  		 	_verEstoquePrecoDeCompra(ing, escolha);
		  		 }
		}else{
			printf("\n\nDigite S para retornar ao menu principal.\n ");
		  	scanf("%s", &ver_novamente);
		}
	}else{
		contador=0;
		system("cls");
		printf("[Codigo]\t\t[Nome do produto]\t\t[Quantidade no estoque]\t\t\t  [Valor de compra]\t\t\t  [Valor de venda]\n");
		for(p =ing; p != NULL; p = p->prox){
			if(p->valor <= preco_max_ingrediente1 && p->valor >= preco_min_ingrediente1){
				printf("\n%4d\t\t\t%15s\t\t\t   %5d%10s\t\t\t%5.2f%10s:R$%5.2f\t\t\t%5.2f%10s:R$%5.2f",
		    			 p->codigo_ingrediente, p->nome,  p->quantidade, p->medida, p->medida_a_ser_vendida, p->medida, p->valor, p->medida_a_ser_vendida, p->medida, p->valor_venda);

	    		contador++;
			}
		}
		if(contador == 0){
		  		 printf("\n\nNenhum produto encontrado. Digite S para pesquisar novamente ou outra tecla para sair:\n ");
		  		 scanf("%s", &ver_novamente);
		  		 if(ver_novamente == 'S'){
		  		 	_verEstoquePrecoDeCompra(ing, escolha);
		  		 }
		}else{
			printf("\n\nDigite S para retornar ao menu principal.\n ");
		  	scanf("%s", &ver_novamente);
		}
	}




}

void _verEstoquePrecoDeVenda(Ingredientes* ing, int escolha){
	system("cls");
	char ver_novamente;
	char preco_max_ingrediente[1000], preco_min_ingrediente[1000];
	float preco_max_ingrediente1, preco_min_ingrediente1;
	int contador;
	Ingredientes* p;
	printf("\n\n\t\t\t*************************************************************");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*               VIZUALIZAÇÃO PREÇO DE VENDA              *");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*************************************************************\n\n");
	printf("\n\t\t\t Informe o menor preço de busca:");
	scanf("%s", preco_min_ingrediente);
	printf("\n\t\t\t Informe o maior preço de busca:");
	scanf("%s", &preco_max_ingrediente);
	preco_min_ingrediente1 = atof(preco_min_ingrediente);
	preco_max_ingrediente1 = atof(preco_max_ingrediente);
	if(escolha == 2){
		for(p =ing; p != NULL; p = p->prox){
			if(p->valor_venda <= preco_max_ingrediente1 && p->valor_venda >= preco_min_ingrediente1){
	    		printf("\nCódigo: %d\nNome do produto: %s\nQuantidade de %s no estoque: %d\nValor de compra a cada %5.2f %s: R$%5.2f\nValor de venda a cada %5.2f %s: R$%5.2f\n\n",
	    			 p->codigo_ingrediente, p->nome, p->medida, p->quantidade, p->medida_a_ser_vendida, p->medida, p->valor, p->medida_a_ser_vendida, p->medida, p->valor_venda);
	    		contador++;
			}
		}
		if(contador == 0){
		  		 printf("\n\nNenhum produto encontrado. Digite S para pesquisar novamente ou outra tecla para sair: \n");
		  		 scanf("%s", &ver_novamente);
		  		 if(ver_novamente == 'S'){
		  		 	_verEstoquePrecoDeVenda(ing, escolha);
		  		 }
		 }else{
		 	printf("\n\nDigite S para retornar ao menu principal.\n ");
		  	scanf("%s", &ver_novamente);
		 }
	}else{
		contador=0;
		system("cls");
		printf("[Codigo]\t\t[Nome do produto]\t\t[Quantidade no estoque]\t\t\t  [Valor de compra]\t\t\t  [Valor de venda]\n");

		for(p =ing; p != NULL; p = p->prox){
			if(p->valor_venda <= preco_max_ingrediente1 && p->valor_venda >= preco_min_ingrediente1){
				printf("\n%4d\t\t\t%15s\t\t\t   %5d%10s\t\t\t%5.2f%10s:R$%5.2f\t\t\t%5.2f%10s:R$%5.2f",
		    			 p->codigo_ingrediente, p->nome,  p->quantidade, p->medida, p->medida_a_ser_vendida, p->medida, p->valor, p->medida_a_ser_vendida, p->medida, p->valor_venda);

	    		contador++;
			}
		}
		if(contador == 0){
		  		 printf("\n\nNenhum produto encontrado. Digite S para pesquisar novamente ou outra tecla para sair: \n");
		  		 scanf("%s", &ver_novamente);
		  		 if(ver_novamente == 'S'){
		  		 	_verEstoquePrecoDeVenda(ing, escolha);
		  		 }
		 }else{
		 	printf("\n\nDigite S para retornar ao menu principal.\n ");
		  	scanf("%s", &ver_novamente);
		 }
	}




}

void _verEstoqueQuantidadeArmazenado(Ingredientes* ing, int escolha){
	system("cls");
	char ver_novamente;
	char quantidade_max_ingrediente[100], quantidade_min_ingrediente[100];
	float quantidade_max_ingrediente1, quantidade_min_ingrediente1;
	int contador;
	Ingredientes* p;
	printf("\n\n\t\t\t*************************************************************");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*            VIZUALIZAÇÃO QUANTIDADE ARMAZENADO           *");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*************************************************************\n\n");
	printf("\n Informe a menor quantidade para busca:");
	scanf("%s", quantidade_min_ingrediente);
	printf("\n Informe a maior quantidade para busca:");
	scanf("%s", quantidade_max_ingrediente);
	quantidade_max_ingrediente1 = atof(quantidade_max_ingrediente);
	quantidade_min_ingrediente1 = atof(quantidade_min_ingrediente);
	if(escolha==2){
		for(p =ing; p != NULL; p = p->prox){
			if(p->quantidade <= quantidade_max_ingrediente1 && p->quantidade >= quantidade_min_ingrediente1){
				printf("\nCódigo: %d\nNome do produto: %s\nQuantidade de %s no estoque: %d\nValor de compra a cada %5.2f %s: R$%5.2f\nValor de venda a cada %5.2f %s: R$%5.2f\n\n",
	    			 p->codigo_ingrediente, p->nome, p->medida, p->quantidade, p->medida_a_ser_vendida, p->medida, p->valor, p->medida_a_ser_vendida, p->medida, p->valor_venda);
	    		contador++;
			}
		}

		if(contador == 0){
		  		 printf("\n\nNenhum produto encontrado. Digite S para pesquisar novamente ou outra tecla para sair:\n ");
		  		 scanf("%s", &ver_novamente);
		  		 if(ver_novamente == 'S'){
		  		 	_verEstoqueQuantidadeArmazenado(ing, escolha);
		  		 }
		 }else{
		 		printf("\n\nDigite S para retornar ao menu principal.\n ");
		  		scanf("%s", &ver_novamente);
		 }
	}else{
		contador=0;
		system("cls");
		printf("[Codigo]\t\t[Nome do produto]\t\t[Quantidade no estoque]\t\t\t  [Valor de compra]\t\t\t  [Valor de venda]\n");

		for(p =ing; p != NULL; p = p->prox){
			if(p->quantidade <= quantidade_max_ingrediente1 && p->quantidade >= quantidade_min_ingrediente1){
				printf("\n%4d\t\t\t%15s\t\t\t   %5d%10s\t\t\t%5.2f%10s:R$%5.2f\t\t\t%5.2f%10s:R$%5.2f",
		    			 p->codigo_ingrediente, p->nome,  p->quantidade, p->medida, p->medida_a_ser_vendida, p->medida, p->valor, p->medida_a_ser_vendida, p->medida, p->valor_venda);

	    		contador++;
			}
		}

		if(contador == 0){
		  		 printf("\nNenhum produto encontrado. Digite S para pesquisar novamente ou outra tecla para sair:\n ");
		  		 scanf("%s", &ver_novamente);
		  		 if(ver_novamente == 'S'){
		  		 	_verEstoqueQuantidadeArmazenado(ing, escolha);
		  		 }
		 }else{
		 		printf("\n\nDigite S para retornar ao menu principal.\n ");
		  		scanf("%s", &ver_novamente);
		 }
	}

}

void _verEstoqueCompleto(Ingredientes* ing, int escolha){
	char ver_novamente;
	printf("\n\n\t\t\t*************************************************************");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*                 ESTOQUE COMPLETO                *");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*************************************************************\n\n");
	system("cls");
	Ingredientes* p;

	if(ing != NULL){
		if(escolha==1){
				printf("[Codigo]\t\t[Nome do produto]\t\t[Quantidade no estoque]\t\t\t  [Valor de compra]\t\t\t  [Valor de venda]\n");
				for(p =ing; p != NULL; p = p->prox){
				printf("\n%4d\t\t\t%15s\t\t\t   %5d%10s\t\t\t%5.2f%10s:R$%5.2f\t\t\t%5.2f%10s:R$%5.2f",
		    			 p->codigo_ingrediente, p->nome,  p->quantidade, p->medida, p->medida_a_ser_vendida, p->medida, p->valor, p->medida_a_ser_vendida, p->medida, p->valor_venda);


				}
			  	printf("\n\n\nDigite S para retornar ao menu principal.\n ");
			  	scanf("%s", &ver_novamente);
		}else{
				for(p =ing; p != NULL; p = p->prox){
					printf("\nCódigo: %d\nNome do produto: %s\nQuantidade de %s no estoque: %d\nValor de compra a cada %5.2f %s: R$%5.2f\nValor de venda a cada %5.2f %s: R$%5.2f\n\n",
		    			 p->codigo_ingrediente, p->nome, p->medida, p->quantidade, p->medida_a_ser_vendida, p->medida, p->valor, p->medida_a_ser_vendida, p->medida, p->valor_venda);

				}
			  	printf("\n\n\nDigite S para retornar ao menu principal: ");
			  	scanf("%s", &ver_novamente);

		}
	}else{
			printf("\n\n\n\nNenhum produto cadastrado no estoque, digite S para retornar ao menu:\n");
			scanf("%s", &ver_novamente);
	}
}



void _insere(Ingredientes** ing, Caixa** caixa) {      //função inserir ingredientes no estoque
	system("cls");
	printf("\n\n\t\t\t*************************************************************");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*                 REPOSIÇÃO DE ESTOQUE                    *");
    printf("\n\t\t\t*                                                           *");
    printf("\n\t\t\t*************************************************************\n\n");
	char escolha[10];
	int escolha1;
	printf("\n\n\t\t[1] - Adicionar novo ingrediente\n\t\t[2] - Adicionar à ingrediente já existente: \n\t\t");
	printf("\n\t\tEscolha:");
	scanf("%s", escolha);
	escolha1 = atoi(escolha);
	switch(escolha1){
		case 1:
			_insereNovo(ing, caixa);
			break;
		case 2:
			_insereExistente(ing, caixa);
			break;
		case 0:
			printf("\n\t\tOpção inválida.\n");
			sleep(3);
			break;
	}


}

void _insereNovo(Ingredientes** ing, Caixa** caixa){
	system("cls");
	struct tm *info;
	time_t segundos;
	int aux;
	char outro_ingrediente;
	int auxQuantidade;
	char auxNome[80], auxMedida[80],auxQuantidade1[10], auxMedida_a_ser_vendida1[10], auxValor1[10], auxValor_venda1[10] ;
	float auxMedida_a_ser_vendida, auxValor, auxValor_venda;

		printf("\n\n\t\t\t*************************************************************");
	    printf("\n\t\t\t*                                                           *");
	    printf("\n\t\t\t*                 REPOSIÇÃO DE ESTOQUE                    *");
	    printf("\n\t\t\t*                                                           *");
	    printf("\n\t\t\t*************************************************************\n\n");
		aux = _verificaUltimoCodigo(*ing);
		printf("\nO código do seu novo ingrediente será: %d\n", aux);
		printf("Nome do ingrediente: ");
		scanf(" %[^\n]", auxNome);
		printf("Tipo de medida ex: kilos, gramas, litros, ml's, latas etc: ");
		scanf(" %[^\n]", auxMedida);
		printf("Quantidade de %s a ser vendido na porção de %s: ", auxMedida, auxNome);     //RECEBENDO NOS AUXILIARES
		scanf(" %[^\n]", auxMedida_a_ser_vendida1);
		printf("Valor de compra de %s %s de %s R$", auxMedida_a_ser_vendida1, auxMedida, auxNome);
		scanf(" %[^\n]", auxValor1);
		printf("Valor de venda de %s %s de %s R$", auxMedida_a_ser_vendida1, auxMedida, auxNome);
		scanf(" %[^\n]", auxValor_venda1);
		printf("Quantidade de %s de %s a serem inseridos no estoque: ", auxMedida, auxNome);
		scanf(" %[^\n]", auxQuantidade1);

		auxMedida_a_ser_vendida = atof(auxMedida_a_ser_vendida1);
		auxValor = atof(auxValor1);
		auxValor_venda = atof(auxValor_venda1);
		auxQuantidade = atoi(auxQuantidade1);

		if((auxMedida_a_ser_vendida > 0) && (auxValor > 0) && (auxValor_venda > 0) && (auxQuantidade > 0)){
			Caixa* cnovo = (Caixa*)malloc(sizeof(Caixa));
			Ingredientes* novo = (Ingredientes*) malloc(sizeof(Ingredientes));

			strcpy(novo->nome, auxNome);       //ADICIONANDO O NOME A LISTA
			strcpy(novo->medida, auxMedida);    //ADICINANDO A MEDIDA
			novo->medida_a_ser_vendida = auxMedida_a_ser_vendida;
			novo->valor = auxValor;
			novo->valor_venda = auxValor_venda;
			novo->quantidade = auxQuantidade;
			novo->codigo_ingrediente = aux;

			novo->prox = *ing;
			*ing = novo;

			float auxiliar = novo->valor/novo->medida_a_ser_vendida;
			cnovo->valorTransicao = auxiliar*novo->quantidade;

			char _tipo[] = "Saida";
			strcpy(cnovo->tipo, _tipo);
			strcpy(cnovo->nome_relatorio, novo->nome);
			time(&segundos);
			info = localtime(&segundos);
			strftime(cnovo->data, 80, "%d/%m/%Y ás %X", info); //guardando em data
			cnovo->dia = info->tm_mday;
			cnovo->mes = info->tm_mon;
			cnovo->ano = info->tm_year;

			cnovo->prox = *caixa;
			*caixa = cnovo;

			printf("\nConcluido com sucesso!\n");
			printf("\nEssa %s lhe custou R$%5.2f. Data: %s \n\n", cnovo->tipo, cnovo->valorTransicao, cnovo->data);
			printf("Digite S para cadastrar outro ingrediente ou outra tecla para sair:");

			scanf("%s", &outro_ingrediente);
					if(outro_ingrediente == 'S'){
					 	_insereNovo(ing, caixa);
					}




		}else{
			printf("\n\nVocê digitou informações inválidas! Digite S para tentar novamente ou outra tecla para sair:");
			scanf("%s", &outro_ingrediente);
			if(outro_ingrediente == 'S'){
				_insereNovo(ing, caixa);
			}
		}



}

void _insereExistente(Ingredientes** ing, Caixa** caixa){
	system("cls");
	struct tm *info;
	time_t segundos;
	char aux1[20], outro_ingrediente;

	Ingredientes* p;
	int codigo, aux, quantidade_adicionada;
	char tentar_novamente;
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                  REPOSIÇÃO DE ESTOQUE                   *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	printf("Informe o codigo do ingrediente: ");
	scanf("%d", &codigo);
	aux = _inEstoque(*ing, codigo);
	if(aux != 0){
		for(p = *ing; p != NULL; p = p->prox ){
			if(p->codigo_ingrediente == codigo){
				printf("Informe a quantidade de %s a ser adicionada em %s:", p->medida, p->nome);
				scanf("%s", aux1);
				quantidade_adicionada = atoi(aux1);
				if(quantidade_adicionada > 0){
					Caixa* cnovo = (Caixa*)malloc(sizeof(Caixa));
					p->quantidade += quantidade_adicionada;

					float auxiliar = p->valor/p->medida_a_ser_vendida;
					cnovo->valorTransicao = auxiliar*quantidade_adicionada;

					char _tipo[] = "Saida";
					strcpy(cnovo->nome_relatorio, p->nome);
					strcpy(cnovo->tipo, _tipo);
					time(&segundos);
					info = localtime(&segundos);
					strftime(cnovo->data, 80, "%d/%m/%Y ás %X", info); //guardando em data
					cnovo->dia = info->tm_mday;
					cnovo->mes = info->tm_mon;
					cnovo->ano = info->tm_year;
					cnovo->prox = *caixa;

					*caixa = cnovo;
					printf("\nEssa %s lhe custou R$%5.2f. Data: %s \n\n", cnovo->tipo, cnovo->valorTransicao, cnovo->data);
					printf("Digite S para cadastrar outro ingrediente ou outra tecla para sair:");

					scanf("%s", &outro_ingrediente);
						if(outro_ingrediente == 'S'){
					 		_insereExistente(ing, caixa);
					}
				}else{
					printf("\n\nQuantidade informada inválida. Retornando ao menu...");
					sleep(3);
				}


			}
		}

	}else{
		printf("\nCodigo não encontrado.Tecle S para tentar novamente ou outra tecla para sair:");
		scanf("%s", &tentar_novamente);
		if(tentar_novamente == 'S'){
			_insereExistente(ing, caixa);
		}


	}





}

void _alteraPrecos(Ingredientes** ing){
	system("cls");
	char tentar_novamente;
	char aux[10], novoPreco[100];
	int aux1, esta_no_estoque;
	float novoPreco1=0;
	Ingredientes* p;
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                 ALTERAR PREÇO PRODUTO                    *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");

	printf("\nInforme o código do produto: ");
	scanf("%s", aux);
	aux1 = atoi(aux);
	esta_no_estoque=_inEstoque(*ing, aux1);
	if(esta_no_estoque != 0){
		for (p=*ing; p!=NULL; p = p->prox){
			if (p->codigo_ingrediente == aux1){
				printf("Novo valor de venda para %5.2f %s de %s: ", p->medida_a_ser_vendida, p->medida, p->nome);
				scanf("%s", novoPreco);
				novoPreco1 = atof(novoPreco);
				if(novoPreco1 != 0){

					p->valor_venda = novoPreco1;
				}else{
					printf("\nValor fornecido inválido.\n");
				}

			}
		}

	}else{
		printf("\nProduto não está cadastrado no estoque. Tecle S para tentar novamente ou outra tecla para sair\n.");
		scanf("%s", &tentar_novamente);
		if(tentar_novamente== 'S'){
			_alteraPrecos(ing);
		}

	}

}

void _removeEstoque(Ingredientes** ing){
	system("cls");
	char nome_ingrediente[81], tentar_novamente, quantidade_a_ser_retirada[100];
	int quantidade_a_ser_retirada1, contador=0;
	Ingredientes* p;
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                 REMOVER DO ESTOQUE                        *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
 	printf("Informa o nome do produto: ");
	scanf("%s", nome_ingrediente);
	for(p= *ing; p != NULL; p= p->prox){
		if(strcmp(nome_ingrediente, p->nome)==0){
			contador++;
			printf("\nDigite quantas(os) %s deseja remover: ", p->medida);
			scanf("%s", quantidade_a_ser_retirada);
			quantidade_a_ser_retirada1 = atoi(quantidade_a_ser_retirada);
			if(quantidade_a_ser_retirada1 <= p->quantidade){
				p->quantidade -= quantidade_a_ser_retirada1;
			}else{
				printf("\nQuantidade informada maior que quantidade no estoque.");
			}

		}
	}
	if(contador == 0){
		printf("\nProduto não está cadastrado no estoque. Tecle S para tentar novamente ou outra tecla para sair.");
		scanf("%s", &tentar_novamente);
		if(tentar_novamente== 'S'){
			_removeEstoque(ing);
		}

	}
}




int _inEstoque(Ingredientes* ing, int aux){
	Ingredientes* p ;
	p=ing;
	int codigo=0;
	if(p== NULL){
		codigo =0;
	}else{

		for(p; p != NULL; p = p->prox ){
			if(p->codigo_ingrediente == aux){
				codigo++;
			}
		}
	}
	return codigo;
}

int _verificaUltimoCodigo(Ingredientes* ing){
	Ingredientes* p ;
	p=ing;
	int codigo=1;
	if(p== NULL){
		codigo =1;
	}else{

		for(p; p != NULL; p = p->prox ){
			if(p->codigo_ingrediente >= codigo){
				codigo = p->codigo_ingrediente+1;
			}
		}
	}
	return codigo;
}


void _relatorios(Ingredientes* ing, Caixa* caixa){
	system("cls");
	char option[10], option2[10];
	int option1, option3;
	printf("\n\t\t\t  _____  ______ _            _______ ____  _____  _____ ____   _____ ");
	printf("\n\t\t\t |  __ \\|  ____| |        /\\|__   __/ __ \\|  __ \\|_   _/ __ \\ / ____|)");
	printf("\n\t\t\t | |__) | |__  | |       /  \\  | | | |  | | |__) | | || |  | | (___  ");
	printf("\n\t\t\t |  _  /|  __| | |      / /\\ \\ | | | |  | |  _  /  | || |  | |\\___ \\ ");
	printf("\n\t\t\t | | \\ \\| |____| |____ / ____ \\| | | |__| | | \\ \\ _| || |__| |____) |");
	printf("\n\t\t\t |_|  \\_\\______|______/_/    \\_\\_|  \\____/|_|  \\_\\_____\\____/|_____/ ");


	printf("\n\n\n\t\t[1] - Ultimo dia\n\t\t[2] - Ultima semana\n\t\t[3] - Ultimo mês\n\t\t[4] - Ultimo semestre\n\t\t[5] - Ultimo ano\n\t\t[6] - Personalizado\n\t\t[7] - Ver tudo \n\t\t");
	printf("\n\t\tEscolha:");
	scanf("%s", option);
	option1 = atoi(option);

	printf("\n\n\t\tDeseja vizualizar de qual maneira:\n\n");
	printf("\t\t[1] - Forma de tabela\n\t\t[2] - Forma corrida\n\t\t");
	printf("\n\t\tEscolha:");
	scanf("%s", &option2);
	option3 = atoi(option2);
	if(option3 == 1 || option3 == 2){
	switch (option1) {
		case 1:
			_relatorioDiario(ing, caixa, option3);
			break;
		case 2:
			_relatorioSemanal(ing, caixa, option3);
			break;
		case 3:
			_relatorioMensal(ing, caixa, option3);
			break;
		case 4:
			_relatorioSemestral(ing, caixa, option3);
			break;
		case 5:
			_relatorioAnual(ing, caixa, option3);
			break;
		case 6:
			_relatorioPersonalizado(ing, caixa, option3);
			break;
		case 7:
			_relatorioTudo(ing, caixa, option3);
			break;
		case 0:
			printf("\n\t\t\tOpção inválida. Retornando ao menu...\n");
			sleep(3);
			break;

		}
	}else{
		printf("\n\t\t\tOpção inválida. Retornando ao menu...\n");
		sleep(3);
	}


}

void _relatorioTudo(Ingredientes* ing, Caixa* caixa, int opcao){
	system("cls");
	char ver_novamente;
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                       FLUXO GERAL                         *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	float entrada, saida;
	Caixa* p;
	if(opcao == 2){
		for(p = caixa; p != NULL; p = p->prox){
			printf("\nNome do produto: %s\nValor da transação: R$%5.2f\nTipo de transação: %s\nData: %s\n\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
				if(strcmp(p->tipo, "Saida")==0){
					saida+= p->valorTransicao;
				}else{
					entrada+= p->valorTransicao;
				}


			}
	}else{
		system("cls");
		printf("\n[Nome do produto]\t\t[Valor da transação]\t\t[Tipo de transação]\t\t\t\t\t        [Data]\n\n");
		for(p = caixa; p != NULL; p = p->prox){
			printf("%15s\t\t\t    R$%5.2f\t\t\t      %10s\t\t\t\t%30s\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
				if(strcmp(p->tipo, "Saida")==0){
					saida+= p->valorTransicao;
				}else{
					entrada+= p->valorTransicao;
				}


			}

	}
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                 RELATÓRIO GERAL                          *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	printf("Você recebeu: R$%5.2f\nVocê gastou: R$%5.2f\nSaldo:R$%5.2f \n\n", entrada, saida, entrada-saida);


	printf("\nDigite S para retornar ao menu principal.\n ");
	 scanf("%s", &ver_novamente);

}

void _relatorioDiario(Ingredientes* ing, Caixa* caixa, int opcao){
	char ver_novamente;
	int aux;
	system("cls");
	float entrada, saida;
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                      FLUXO ULTIMO DIA                     *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	int dataAComparar1, dataSistema1;
	dataSistema1 = dataSistema();
	Caixa* p;
	if(opcao == 2){
		for(p = caixa; p != NULL; p = p->prox){
			dataAComparar1 = dataAComparar(p);
			if(dataSistema1 - dataAComparar1 == 0 || dataSistema1 - dataAComparar1 ==1 ){
				printf("\nNome do produto: %s\nValor da transação: R$%5.2f\nTipo de transação: %s\nData: %s\n\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
					if(strcmp(p->tipo, "Saida")==0){
						saida+= p->valorTransicao;
					}else{
						entrada+= p->valorTransicao;
					}
			}


			}
	}else{
		system("cls");
		printf("\n[Nome do produto]\t\t[Valor da transação]\t\t[Tipo de transação]\t\t\t\t\t        [Data]\n\n");
		for(p = caixa; p != NULL; p = p->prox){
					dataAComparar1 = dataAComparar(p);
					if(dataSistema1 - dataAComparar1 == 0 || dataSistema1 - dataAComparar1 ==1 ){
						printf("%15s\t\t\t    R$%5.2f\t\t\t      %10s\t\t\t\t%30s\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
							if(strcmp(p->tipo, "Saida")==0){
								saida+= p->valorTransicao;
							}else{
								entrada+= p->valorTransicao;
							}
					}


					}

	}
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                  RELATÓRIO ULTIMO DIA                    *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	printf("Você recebeu: R$%5.2f\nVocê gastou: R$%5.2f\nSaldo:R$%5.2f \n\n", entrada, saida, entrada-saida);
	printf("\nDigite S para retornar ao menu principal.\n ");
	scanf("%s", &ver_novamente);



}

void _relatorioSemanal(Ingredientes* ing, Caixa* caixa, int opcao){
	char ver_novamente;
	int aux;
	system("cls");
	float entrada, saida;
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                     FLUXO ULTIMA SEMANA                   *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	int dataAComparar1, dataSistema1;
	dataSistema1 = dataSistema();
	Caixa* p;
	if(opcao == 2){
		for(p = caixa; p != NULL; p = p->prox){
			dataAComparar1 = dataAComparar(p);
			if(dataSistema1 - dataAComparar1 <= 7){
				printf("\nNome do produto: %s\nValor da transação: R$%5.2f\nTipo de transação: %s\nData: %s\n\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
					if(strcmp(p->tipo, "Saida")==0){
						saida+= p->valorTransicao;
					}else{
						entrada+= p->valorTransicao;
					}
			}


			}
	}else{
		system("cls");
		printf("\n[Nome do produto]\t\t[Valor da transação]\t\t[Tipo de transação]\t\t\t\t\t        [Data]\n\n");
		for(p = caixa; p != NULL; p = p->prox){
			dataAComparar1 = dataAComparar(p);
			if(dataSistema1 - dataAComparar1 <= 7){
					printf("%15s\t\t\t    R$%5.2f\t\t\t      %10s\t\t\t\t%30s\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
					if(strcmp(p->tipo, "Saida")==0){
						saida+= p->valorTransicao;
					}else{
						entrada+= p->valorTransicao;
					}
			}


			}

	}
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                 RELATORIO ULTIMA SEMANA                   *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	printf("Você recebeu: R$%5.2f\nVocê gastou: R$%5.2f\nSaldo:R$%5.2f \n\n", entrada, saida, entrada-saida);

	printf("\nDigite S para retornar ao menu principal.\n ");
	scanf("%s", &ver_novamente);



}

void _relatorioMensal(Ingredientes* ing, Caixa* caixa, int opcao){
	int aux;
	system("cls");
	char ver_novamente;
	float entrada, saida;
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                     FLUXO ULTIMO MÊS                     *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	int dataAComparar1, dataSistema1;
	dataSistema1 = dataSistema();
	Caixa* p;
	if(opcao == 2){
		for(p = caixa; p != NULL; p = p->prox){
			dataAComparar1 = dataAComparar(p);
			if(dataSistema1 - dataAComparar1 <= 31){
				printf("\nNome do produto: %s\nValor da transação: R$%5.2f\nTipo de transação: %s\nData: %s\n\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
					if(strcmp(p->tipo, "Saida")==0){
						saida+= p->valorTransicao;
					}else{
						entrada+= p->valorTransicao;
					}
			}


			}
	}else{
		system("cls");
		printf("\n[Nome do produto]\t\t[Valor da transação]\t\t[Tipo de transação]\t\t\t\t\t        [Data]\n\n");
		for(p = caixa; p != NULL; p = p->prox){
			dataAComparar1 = dataAComparar(p);
			if(dataSistema1 - dataAComparar1 <= 31){
					printf("%15s\t\t\t    R$%5.2f\t\t\t      %10s\t\t\t\t%30s\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
					if(strcmp(p->tipo, "Saida")==0){
						saida+= p->valorTransicao;
					}else{
						entrada+= p->valorTransicao;
					}
			}


			}

	}
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                    FLUXO ULTIMO MÊS                      *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	printf("Você recebeu: R$%5.2f\nVocê gastou: R$%5.2f\nSaldo:R$%5.2f \n\n", entrada, saida, entrada-saida);
	printf("\nDigite S para retornar ao menu principal.\n ");
	scanf("%s", &ver_novamente);



}

void _relatorioSemestral(Ingredientes* ing, Caixa* caixa, int opcao){
	int aux;
	system("cls");
	float entrada, saida;
	char ver_novamente;
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                  FLUXO ULTIMO SEMESTRE                    *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	int dataAComparar1, dataSistema1;
	dataSistema1 = dataSistema();
	Caixa* p;
	if(opcao == 2){
		for(p = caixa; p != NULL; p = p->prox){
			dataAComparar1 = dataAComparar(p);
			if(dataSistema1 - dataAComparar1 <= 182){
				printf("\nNome do produto: %s\nValor da transação: R$%5.2f\nTipo de transação: %s\nData: %s\n\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
					if(strcmp(p->tipo, "Saida")==0){
						saida+= p->valorTransicao;
					}else{
						entrada+= p->valorTransicao;
					}
			}


			}
	}else{
		system("cls");
		printf("\n[Nome do produto]\t\t[Valor da transação]\t\t[Tipo de transação]\t\t\t\t\t        [Data]\n\n");
			for(p = caixa; p != NULL; p = p->prox){
				dataAComparar1 = dataAComparar(p);
				if(dataSistema1 - dataAComparar1 <= 182){
					printf("%15s\t\t\t    R$%5.2f\t\t\t      %10s\t\t\t\t%30s\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
						if(strcmp(p->tipo, "Saida")==0){
							saida+= p->valorTransicao;
						}else{
							entrada+= p->valorTransicao;
						}
				}


			}

	}
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                 RELATORIO ULTIMO SEMESTRE                 *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	printf("Você recebeu: R$%5.2f\nVocê gastou: R$%5.2f\nSaldo:R$%5.2f \n\n", entrada, saida, entrada-saida);

	printf("\nDigite S para retornar ao menu principal.\n ");
	scanf("%s", &ver_novamente);



}

void _relatorioAnual(Ingredientes* ing, Caixa* caixa, int opcao){
	int aux;
	system("cls");
	float entrada, saida;
	char ver_novamente;
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                      FLUXO ULTIMO ANO                     *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	int dataAComparar1, dataSistema1;
	dataSistema1 = dataSistema();
	Caixa* p;
	if(opcao == 2){
		for(p = caixa; p != NULL; p = p->prox){
			dataAComparar1 = dataAComparar(p);
			if(dataSistema1 - dataAComparar1 <= 365){
				printf("\nNome do produto: %s\nValor da transação: R$%5.2f\nTipo de transação: %s\nData: %s\n\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
					if(strcmp(p->tipo, "Saida")==0){
						saida+= p->valorTransicao;
					}else{
						entrada+= p->valorTransicao;
					}
			}


			}
	}else{
		system("cls");
		printf("\n[Nome do produto]\t\t[Valor da transação]\t\t[Tipo de transação]\t\t\t\t\t        [Data]\n\n");
		for(p = caixa; p != NULL; p = p->prox){
			dataAComparar1 = dataAComparar(p);
			if(dataSistema1 - dataAComparar1 <= 365){
					printf("%15s\t\t\t    R$%5.2f\t\t\t      %10s\t\t\t\t%30s\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
					if(strcmp(p->tipo, "Saida")==0){
						saida+= p->valorTransicao;
					}else{
						entrada+= p->valorTransicao;
					}
			}


			}

	}
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                   RELATORIO ULTIMO ANO                    *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	printf("Você recebeu: R$%5.2f\nVocê gastou: R$%5.2f\nSaldo:R$%5.2f \n\n", entrada, saida, entrada-saida);
	printf("\nDigite S para retornar ao menu principal.\n ");
	scanf("%s", &ver_novamente);


}

void _relatorioPersonalizado(Ingredientes* ing, Caixa* caixa, int opcao){
	int aux, data;
	char data1[20], data2[20], tentar_novamente, ver_novamente;
	system("cls");
	float entrada, saida;
	printf("\n\n\t\t\t*************************************************************");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*                 RELATORIO PERSONALIZADO                   *");
	printf("\n\t\t\t*                                                           *");
	printf("\n\t\t\t*************************************************************\n\n");
	printf("\nInforme a primeira data no formato DD/MM/AAAA:");
	scanf("%s", data1);
	printf("\nInforme a segunda data no formato DD/MM/AAAA:");
	scanf("%s", data2);
	int dataAComparar1, dataAComparar2;
	aux = validaData(data1, data2, &dataAComparar1, &dataAComparar2);

	if(aux == 1){
		Caixa* p;
		printf("\n\n\t\t\t*************************************************************");
		printf("\n\t\t\t*                                                           *");
		printf("\n\t\t\t*               FLUXO ENTRE AS DATAS FORNECIDAS             *");
		printf("\n\t\t\t*                                                           *");
		printf("\n\t\t\t*************************************************************\n\n");
		if(opcao == 2){
			for(p = caixa; p != NULL; p = p->prox){
					data = dataAComparar(p);
					if(data<=dataAComparar2 && data >= dataAComparar1){
						printf("\nNome do produto: %s\nValor da transação: R$%5.2f\nTipo de transação: %s\nData: %s\n\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
							if(strcmp(p->tipo, "Saida")==0){
								saida+= p->valorTransicao;
							}else{
								entrada+= p->valorTransicao;
							}
					}


					}
				printf("\n\n*** RELATÓRIO ***\n\n");
				printf("\n\nVocê recebeu: R$%5.2f\nVocê gastou: R$%5.2f\nSaldo:R$%5.2f \n\n", entrada, saida, entrada-saida);

				printf("\nDigite S para retornar ao menu principal.\n ");
			 	scanf("%s", &ver_novamente);
		}else{
			system("cls");
			printf("\n[Nome do produto]\t\t[Valor da transação]\t\t[Tipo de transação]\t\t\t\t\t        [Data]\n\n");
			for(p = caixa; p != NULL; p = p->prox){
					data = dataAComparar(p);
					if(data<=dataAComparar2 && data >= dataAComparar1){
						printf("%15s\t\t\t    R$%5.2f\t\t\t      %10s\t\t\t\t%30s\n", p->nome_relatorio, p->valorTransicao, p->tipo, p->data);
							if(strcmp(p->tipo, "Saida")==0){
								saida+= p->valorTransicao;
							}else{
								entrada+= p->valorTransicao;
							}
					}


					}
				printf("\n\n*** RELATÓRIO ***\n\n");
				printf("\n\nVocê recebeu: R$%5.2f\nVocê gastou: R$%5.2f\nSaldo:R$%5.2f \n\n", entrada, saida, entrada-saida);

				printf("\nDigite S para retornar ao menu principal.\n ");
			 	scanf("%s", &ver_novamente);

		}
	}else{
		printf("Datas fornecidas inválidas! Digite S para pesquisar novamente ou outra tecla para sair:");
		scanf("%s", &tentar_novamente);
		if(tentar_novamente== 'S'){
			_relatorioPersonalizado(ing, caixa, opcao);
		}
	}
}

int dataAComparar(Caixa*p){
	struct tm t;
	t.tm_mday = p->dia;
	t.tm_mon = p->mes;
	t.tm_year = p->ano;
	t.tm_hour = 0;
	t.tm_min= 0;
	t.tm_sec = 1;
	t.tm_isdst = -1;
	int retorno = mktime(&t);
	return retorno/86400;


}

int dataSistema(){
	struct tm* t;
	time_t rawtime;
	time(&rawtime);
	t= localtime(&rawtime);
	int retorno = mktime(t);
	return retorno/86400;

}

int validaData(char *data1, char *data2, int *dataAComparar1, int *dataAComparar2){
	struct tm t;
	int contador = 0, retorno;
	char *auxDia, *auxMes, *auxAno, *auxDiaDois, *auxMesDois, *auxAnoDois;
	auxDia = strtok(data1, "/");
	auxMes = strtok(NULL, "/");
	auxAno = strtok(NULL, "/");

	auxDiaDois = strtok(data2, "/");
	auxMesDois = strtok(NULL, "/");
	auxAnoDois = strtok(NULL, "/");

	int auxDia1, auxMes1, auxAno1, auxDia2, auxMes2, auxAno2;

	auxDia1 = atoi(auxDia);
	auxMes1 = atoi(auxMes);
	auxAno1 = atoi(auxAno);
	auxDia2 = atoi(auxDiaDois);
	auxMes2 = atoi(auxMesDois);
	auxAno2 = atoi(auxAnoDois);

	auxAno1-=1900;
	auxMes1--;
	t.tm_mday = auxDia1;
	t.tm_mon = auxMes1;
	t.tm_year = auxAno1;
	t.tm_hour = 0;
	t.tm_min= 0;
	t.tm_sec = 1;
	t.tm_isdst = -1;
	retorno = mktime(&t);
	*dataAComparar1 = retorno/86400;
	///////////////////////////////

	auxAno2-=1900;
	auxMes2--;
	t.tm_mday = auxDia2;
	t.tm_mon = auxMes2;
	t.tm_year = auxAno2;
	t.tm_hour = 0;
	t.tm_min= 0;
	t.tm_sec = 1;
	t.tm_isdst = -1;
	retorno = mktime(&t);
	*dataAComparar2 = retorno/86400;

	auxAno1+=1900;
	auxAno2+=1900;
	auxMes1++;
	auxMes2++;



	if((auxDia1 > 31 || auxDia1 <=0 ) || (auxDia2 > 31 || auxDia2 <=0 )){
		contador++;
	}

	if((auxMes1 > 12 || auxMes1 <=0 ) || (auxMes2 > 12 || auxMes2 <=0 )){
		contador++;
	}

	if(auxAno1 <=0 || auxAno2 <=0){
		contador++;
	}

	if(contador == 0){
		return 1;
	}else{
		return 0;
	}


}

void informacoes(void){
	char menu;
	system("cls");
	printf("\n\t\t\t\t******************************************\t\t\n");
	printf("\t\t\t\t*                                        *\t\t\n");
	printf("\t\t\t\t* Sistema de gerenciamento de lanchonete *\t\t\n");
	printf("\t\t\t\t*                                        *\t\t\n");
	printf("\t\t\t\t******************************************\t\t\n");

	printf("\n\n\n\t\t VERSÃO: 1.0 \t\t\n");
	printf("\t\t DESENVOLVIDO POR MATEUS MEDEIROS DE ARAÚJO E LAIO DE ALENCAR ANDRADE \t\t\n");
	printf("\t\t PARA PROJETO FINAL DA DISCIPLINA DE PROGRAMAÇÃO \t\t\n");
	printf("\t\t PROFESSOR ALEXANDRE QUEIROZ \t\t\n");
	printf("\t\t UFRN/CERES CAMPUS CAICÓ, BS1 2017.2 \t\t\n\n");
	printf("\t\t DATA DE TÉRMINO: 01/12/2017 \t\t\n\n\n");
	printf("\t\t CÓDIGO DISPONÍVEL EM: https://gist.github.com/mathmed/89693c2a58dd0296286ca1b450b0b655 \t\t\n");
	
	printf("\n\n\n\t\t\tDigite alguma tecla para voltar ao menu:");
	scanf("%s", &menu);

}

