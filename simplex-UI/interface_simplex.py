import customtkinter as ctk
import numpy as np

# Configurações de Aparência da UI
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppSimplex(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Resolutor Simplex - Programação Linear")
        self.geometry("850x700")

        # Lista para armazenar os componentes visuais das restrições
        self.entradas_restricoes = []

        # --- TÍTULO ---
        self.label_titulo = ctk.CTkLabel(self, text="Algoritmo Simplex (Maximização)", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_titulo.pack(pady=15)

        # --- FRAME: FUNÇÃO OBJETIVO ---
        self.frame_c = ctk.CTkFrame(self)
        self.frame_c.pack(pady=10, padx=20, fill="x")

        self.lbl_c = ctk.CTkLabel(self.frame_c, text="Coeficientes da Função Objetivo (Z):", font=ctk.CTkFont(weight="bold"))
        self.lbl_c.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.entry_c = ctk.CTkEntry(self.frame_c, placeholder_text="Ex: 3 5 (para 3x1 + 5x2)", width=500)
        self.entry_c.grid(row=1, column=0, padx=10, pady=10, sticky="we")

        # --- FRAME: RESTRIÇÕES (Com Scroll) ---
        self.label_restr = ctk.CTkLabel(self, text="Restrições (A e b):", font=ctk.CTkFont(weight="bold"))
        self.label_restr.pack(pady=(10, 0))

        self.scroll_frame = ctk.CTkScrollableFrame(self, height=250)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Botões de Controle de Linhas
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=5)

        self.btn_add = ctk.CTkButton(self.btn_frame, text="+ Adicionar Restrição", command=self.add_linha_restricao, fg_color="green", hover_color="#006400")
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_rem = ctk.CTkButton(self.btn_frame, text="- Remover Última", command=self.rem_linha_restricao, fg_color="red", hover_color="#8B0000")
        self.btn_rem.grid(row=0, column=1, padx=5)

        # Adiciona 2 restrições iniciais por padrão
        self.add_linha_restricao()
        self.add_linha_restricao()

        # --- BOTÃO RESOLVER ---
        self.btn_resolver = ctk.CTkButton(self, text="CALCULAR SOLUÇÃO ÓTIMA", font=ctk.CTkFont(size=16, weight="bold"), height=45, command=self.executar_calculo)
        self.btn_resolver.pack(pady=15, padx=20, fill="x")

        # --- ÁREA DE RESULTADO ---
        self.txt_resultado = ctk.CTkTextbox(self, height=150, font=ctk.CTkFont(family="Consolas", size=14))
        self.txt_resultado.pack(pady=10, padx=20, fill="both")
        self.txt_resultado.insert("0.0", "Os resultados aparecerão aqui...")
        self.txt_resultado.configure(state="disabled")

    def add_linha_restricao(self):
        row_idx = len(self.entradas_restricoes)
        frame = ctk.CTkFrame(self.scroll_frame)
        frame.pack(fill="x", pady=5)

        lbl = ctk.CTkLabel(frame, text=f"R{row_idx+1}:", width=40)
        lbl.pack(side="left", padx=5)

        entry_a = ctk.CTkEntry(frame, placeholder_text="Coeficientes A (Ex: 1 2)", width=300)
        entry_a.pack(side="left", padx=5, expand=True, fill="x")

        # Menu drop-down para selecionar o sinal da restrição
        menu_sinal = ctk.CTkOptionMenu(frame, values=["<=", ">="], width=70)
        menu_sinal.pack(side="left", padx=5)

        entry_b = ctk.CTkEntry(frame, placeholder_text="b", width=80)
        entry_b.pack(side="left", padx=5)

        self.entradas_restricoes.append({
            "frame": frame, 
            "A": entry_a, 
            "sinal": menu_sinal, 
            "b": entry_b
        })

    def rem_linha_restricao(self):
        if len(self.entradas_restricoes) > 1:
            item = self.entradas_restricoes.pop()
            item["frame"].destroy()

    def mostrar_log(self, mensagem):
        self.txt_resultado.configure(state="normal")
        self.txt_resultado.delete("1.0", "end")
        self.txt_resultado.insert("0.0", mensagem)  # Corrigido aqui (removido o 'message=')
        self.txt_resultado.configure(state="disabled")

    # SUA LÓGICA ORIGINAL DO SIMPLEX
    def simplex_core(self, c, A, b):
        num_restricoes, num_variaveis = A.shape
        tableau = np.zeros((num_restricoes + 1, num_variaveis + num_restricoes + 1))
        tableau[:num_restricoes, :num_variaveis] = A
        tableau[:num_restricoes, -1] = b
        tableau[:num_restricoes, num_variaveis:num_variaveis + num_restricoes] = np.eye(num_restricoes)
        tableau[-1, :num_variaveis] = -c
        
        iteracao = 1
        while True:
            if np.all(np.round(tableau[-1, :-1], 10) >= 0):
                break
            coluna_pivo = np.argmin(tableau[-1, :-1])
            razoes = []
            for i in range(num_restricoes):
                if tableau[i, coluna_pivo] > 0:
                    razoes.append(tableau[i, -1] / tableau[i, coluna_pivo])
                else:
                    razoes.append(np.inf)
            
            linha_pivo = np.argmin(razoes)
            if razoes[linha_pivo] == np.inf:
                raise ValueError("O problema tem solução ilimitada (região viável não é limitada).")
            
            elemento_pivo = tableau[linha_pivo, coluna_pivo] # Corrigido aqui ('coluna_pivo' em vez de 'column_pivo')
            tableau[linha_pivo, :] /= elemento_pivo
            for i in range(num_restricoes + 1):
                if i != linha_pivo:
                    fator = tableau[i, coluna_pivo]
                    tableau[i, :] -= fator * tableau[linha_pivo, :]
            iteracao += 1

        solucao = np.zeros(num_variaveis)
        for j in range(num_variaveis):
            coluna = tableau[:-1, j]
            if np.count_nonzero(np.round(coluna, 10) == 1) == 1 and np.count_nonzero(np.round(coluna, 10) == 0) == num_restricoes - 1:
                linha_indice = np.where(np.round(coluna, 10) == 1)[0][0]
                solucao[j] = tableau[linha_indice, -1]
        
        return solucao, tableau[-1, -1], iteracao

    def executar_calculo(self):
        try:
            # Capturar Função Objetivo
            c_raw = self.entry_c.get().split()
            if not c_raw:
                raise Exception("A função objetivo não pode estar vazia.")
            c = np.array([float(x) for x in c_raw])

            # Capturar Restrições
            A_list = []
            b_list = []
            for idx, item in enumerate(self.entradas_restricoes):
                a_vals = [float(x) for x in item["A"].get().split()]
                b_val = float(item["b"].get())
                sinal = item["sinal"].get()
                
                if len(a_vals) != len(c):
                    raise Exception(f"A restrição R{idx+1} possui {len(a_vals)} variáveis, mas a função objetivo possui {len(c)}.")
                
                # --- TRATAMENTO DO SINAL >= ---
                if sinal == ">=":
                    a_vals = [-x for x in a_vals]
                    b_val = -b_val

                A_list.append(a_vals)
                b_list.append(b_val)

            A = np.array(A_list)
            b = np.array(b_list)

            # Chamar seu algoritmo original
            solucao, z_otimo, iters = self.simplex_core(c, A, b)

            # Formatar Resultado para a UI
            res_txt = "=== SUCESSO: SOLUÇÃO ENCONTRADA ===\n"
            res_txt += f"Iterações realizadas: {iters - 1}\n"
            res_txt += f"Valor ótimo (Z): {z_otimo:.4f}\n"
            res_txt += "Valores das variáveis de decisão:\n"
            for i, v in enumerate(solucao):
                res_txt += f"  x_{i+1} = {v:.4f}\n"
            
            self.mostrar_log(res_txt)

        except ValueError:
            self.mostrar_log("ERRO: Verifique se todos os campos contêm apenas números separados por espaço.")
        except Exception as e:
            self.mostrar_log(f"ERRO: {str(e)}")

if __name__ == "__main__":
    app = AppSimplex()
    app.mainloop()