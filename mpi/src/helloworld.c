#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char** argv) {
    int rank, size;               // Identificador do processo e número total de processos
    int *array_local, *array;     
    int soma_local, soma;       
    int tamanho = 8;             
    int tamanho_local;            // Tamanho da parte que cada processo vai receber

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Calcula quantos elementos cada processo receberá (assumindo divisão exata)
    tamanho_local = tamanho / size;
    array_local = (int*)malloc(tamanho_local * sizeof(int));

    // Processo 0 cria e preenche o array completo, depois exibe
    if (rank == 0) {
        array = (int*)malloc(tamanho * sizeof(int));
        printf("Array: ");
        for (int i = 0; i < tamanho; i++) {
            array[i] = i + 1;         
            printf("%d ", array[i]);
        }
        printf("\n");
    }

    // Distribui pedaços = do array para todos os processos
    MPI_Scatter(array, tamanho_local, MPI_INT,
                array_local, tamanho_local, MPI_INT,
                0, MPI_COMM_WORLD);

    // Cada processo calcula sua soma local e imprime o pedaço recebido
    soma_local = 0;
    printf("Array recebido pelo rank %2d: ", rank);
    for (int i = 0; i < tamanho_local; i++) {
        printf("%3d ", array_local[i]);
        soma_local += array_local[i];
    }
    printf("-- soma local: %4d\n", soma_local);

    // Reduz todas as somas locais para uma soma global no processo 0
    MPI_Reduce(&soma_local, &soma, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    // Processo 0 exibe o resultado final e valida com a fórmula da soma de PA
    if (rank == 0) {
        sleep(1);   // Pausa para tentar organizar a saída 
        printf("Soma do array: %d\n", soma);
        printf("Valor esperado: %d\n", tamanho * (tamanho + 1) / 2);
        free(array);   
    }

    // Libera a memória local e finaliza o MPI
    free(array_local);
    MPI_Finalize();
    return 0;
}