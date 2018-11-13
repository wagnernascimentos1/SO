import os, sys

comando = [ "/usr/bin/bc" ]
firefox = [ "/usr/local/bin/firefox" ]
mousepad = [ "/usr/local/bin/mousepad" ]   

rpaifilho, wpaifilho = os.pipe();
rfilhopai, wfilhopai = os.pipe();
option = ""
while option != "q":
	option = input("""
	    Digite w para a calc;
	    Digite s para o firefox
	    Digite a para o mousepad;
	    Digite q para sair:""")

	if option == "w":
		rpaifilho, wpaifilho = os.pipe();
		rfilhopai, wfilhopai = os.pipe();
		processid = os.fork()
		if processid: #Processo pai
			os.close(rpaifilho); # Fecha o descritor desnecessário
			escrita = os.fdopen(wpaifilho, 'w') # reabre como uma stream de escrita

			os.close(wfilhopai); # Fecha o descritor desnecessário
			leitura = os.fdopen(rfilhopai, 'r') # reabre como uma stream de leitura

			print("Digite uma expressão (quit para sair): ")
			linha = sys.stdin.readline()

			while linha != "":
				if linha == "\n": #Se apertou enter leia novamente
					linha = sys.stdin.readline()
					continue

				escrita.write(linha)
				escrita.flush()

				linha = leitura.readline()
				if linha != "":
					print("Resposta: %s" % linha)
				else:
					break
				print("Digite uma expressão (quit para sair): ")
				linha = sys.stdin.readline()

		else: # Processo filho
			os.dup2(rpaifilho, sys.stdin.fileno()) # Associa a leitura pai-filho com a entrada padrão
			os.close(wpaifilho) # Fecha o descritor desnecessário

			os.dup2(wfilhopai, sys.stdout.fileno()) # Associa a escrita filho-pai com a saida padrao       
			os.close(rfilhopai) # Fecha o descritor desnecessário

			# Código para substituir a imagem do processo
			os.execve(comando[0], comando, os.environ) # Substitui a imagem do programa pela calculadora bc

	if option == "s":
			newpid=os.fork()
			if newpid == 0:
				os.execve(firefox[0], firefox, os.environ) 

	if option == "a":
			newpid=os.fork()
			if newpid == 0:
				os.execve(mousepad[0], mousepad, os.environ)
	else: 
		print()
