import streamlit as st  
import pandas as pd  
import datetime  
import plotly.express as px  
import plotly.graph_objects as go  

class EstudoTracker:  
    def __init__(self):  
        self.data_inicio = datetime.datetime.now()  
        self.estrutura_estudos = {  
            "CONHECIMENTOS_GERAIS": {  
                "LINGUA_PORTUGUESA": [  
                    "Compreensão e interpretação de textos",  
                    "Reconhecimento de tipos textuais",  
                    "Domínio da ortografia oficial",  
                    "Mecanismos de coesão textual",  
                    "Estrutura morfossintática",  
                    "Reescrita de frases e parágrafos"  
                ],  
                "MATEMATICA": [  
                    "Conjuntos numéricos",  
                    "Sistema legal de medidas",  
                    "Razões e proporções",  
                    "Equações e inequações",  
                    "Matemática financeira",  
                    "Geometria plana e espacial"  
                ],  
                "LINGUA_INGLESA": [  
                    "Compreensão de textos",  
                    "Itens gramaticais",  
                    "Versão Português-Inglês",  
                    "Tradução Inglês-Português"  
                ],  
                "LOGICA_ESTATISTICA": [  
                    "Estruturas lógicas",  
                    "Lógica de argumentação",  
                    "Lógica sentencial",  
                    "População e amostra",  
                    "Medidas estatísticas",  
                    "Probabilidade"  
                ]  
            },  
            "CONHECIMENTOS_COMPLEMENTARES": {  
                "CIENCIAS_EXATAS": [  
                    "Agricultura 5.0",  
                    "Métodos de análise multivariada",  
                    "Estrutura de dados",  
                    "Fundamentos de estatística",  
                    "Geoprocessamento"  
                ],  
                "GESTAO_INFORMACAO": [  
                    "Administração de sistemas",  
                    "Arquitetura de rede",  
                    "Computação em nuvem",  
                    "Segurança da informação",  
                    "Inteligência artificial"  
                ]  
            },  
            "CONHECIMENTOS_ESPECIFICOS": {  
                "TECNICO_TI": [  
                    "Conceitos de hardware",  
                    "Manutenção de redes",  
                    "Banco de dados",  
                    "Infraestrutura de TI",  
                    "Suporte técnico"  
                ]  
            }  
        }  

        # Inicializar o estado da sessão se não existir  
        if 'progresso' not in st.session_state:  
            st.session_state.progresso = self._inicializar_progresso()  

    def _inicializar_progresso(self):  
        progresso = {}  
        for area, subareas in self.estrutura_estudos.items():  
            progresso[area] = {}  
            for subarea, topicos in subareas.items():  
                progresso[area][subarea] = {}  
                for topico in topicos:  
                    progresso[area][subarea][topico] = {  
                        "estudado": False,  
                        "exercicios": False,  
                        "revisao1": False,  
                        "revisao2": False,  
                        "revisao3": False,  
                        "data_estudo": None,  
                        "data_exercicios": None,  
                        "data_revisao1": None,  
                        "data_revisao2": None,  
                        "data_revisao3": None  
                    }  
        return progresso  

    def marcar_progresso(self, area, subarea, topico, tipo_progresso):  
        """Marca o progresso de um tópico específico"""  
        if tipo_progresso not in ['estudado', 'exercicios', 'revisao1', 'revisao2', 'revisao3']:  
            st.error("Tipo de progresso inválido")  
            return  

        st.session_state.progresso[area][subarea][topico][tipo_progresso] = True  
        st.session_state.progresso[area][subarea][topico][f"data_{tipo_progresso}"] = datetime.datetime.now().strftime("%Y-%m-%d")  

    def gerar_relatorio(self):  
        """Gera um relatório detalhado do progresso"""  
        relatorio = []  
        for area, subareas in st.session_state.progresso.items():  
            for subarea, topicos in subareas.items():  
                for topico, status in topicos.items():  
                    relatorio.append({  
                        'Area': area,  
                        'Subarea': subarea,  
                        'Topico': topico,  
                        'Estudado': status['estudado'],  
                        'Exercicios': status['exercicios'],  
                        'Revisao1': status['revisao1'],  
                        'Revisao2': status['revisao2'],  
                        'Revisao3': status['revisao3'],  
                        'Data_Estudo': status['data_estudo'],  
                        'Data_Exercicios': status['data_exercicios'],  
                        'Data_Revisao1': status['data_revisao1'],  
                        'Data_Revisao2': status['data_revisao2'],  
                        'Data_Revisao3': status['data_revisao3']  
                    })  
        return pd.DataFrame(relatorio)  

    def calcular_progresso_geral(self):  
        """Calcula o percentual de progresso geral dos estudos"""  
        total_topicos = 0  
        topicos_estudados = 0  
        exercicios_feitos = 0  
        revisoes_feitas = 0  

        for area, subareas in st.session_state.progresso.items():  
            for subarea, topicos in subareas.items():  
                for topico, status in topicos.items():  
                    total_topicos += 1  
                    if status['estudado']: topicos_estudados += 1  
                    if status['exercicios']: exercicios_feitos += 1  
                    revisoes = sum([status['revisao1'], status['revisao2'], status['revisao3']])  
                    revisoes_feitas += revisoes  

        return {  
            'Progresso_Estudo': (topicos_estudados / total_topicos) * 100,  
            'Progresso_Exercicios': (exercicios_feitos / total_topicos) * 100,  
            'Media_Revisoes': (revisoes_feitas / (total_topicos * 3)) * 100  
        }  

def main():  
    st.set_page_config(  
        page_title="Tracker de Estudos EMBRAPA",  
        page_icon="📚",  
        layout="wide",  
        initial_sidebar_state="expanded"  
    )  

    st.title("📚 Tracker de Estudos - Concurso EMBRAPA")  

    # Inicializar o tracker  
    tracker = EstudoTracker()  

    # Sidebar para navegação  
    st.sidebar.title("Navegação")  
    pagina = st.sidebar.radio(  
        "Escolha uma seção:",  
        ["Marcar Progresso", "Relatório de Progresso", "Estatísticas"]  
    )  

    if pagina == "Marcar Progresso":  
        st.header("Marcar Progresso")  

        col1, col2, col3, col4 = st.columns(4)  

        with col1:  
            area = st.selectbox("Área:", list(tracker.estrutura_estudos.keys()))  

        with col2:  
            subarea = st.selectbox("Subárea:", list(tracker.estrutura_estudos[area].keys()))  

        with col3:  
            topico = st.selectbox("Tópico:", tracker.estrutura_estudos[area][subarea])  

        with col4:  
            tipo_progresso = st.selectbox(  
                "Tipo de Progresso:",  
                ['estudado', 'exercicios', 'revisao1', 'revisao2', 'revisao3']  
            )  

        if st.button("Marcar como Concluído", type="primary"):  
            tracker.marcar_progresso(area, subarea, topico, tipo_progresso)  
            st.success(f"✅ {topico} marcado como {tipo_progresso}!")  

    elif pagina == "Relatório de Progresso":  
        st.header("Relatório de Progresso")  

        relatorio = tracker.gerar_relatorio()  

        # Filtros  
        col1, col2 = st.columns(2)  
        with col1:  
            filtro_area = st.multiselect("Filtrar por Área:", relatorio['Area'].unique())  
        with col2:  
            filtro_subarea = st.multiselect("Filtrar por Subárea:", relatorio['Subarea'].unique())  

        # Aplicar filtros  
        df_filtrado = relatorio.copy()  
        if filtro_area:  
            df_filtrado = df_filtrado[df_filtrado['Area'].isin(filtro_area)]  
        if filtro_subarea:  
            df_filtrado = df_filtrado[df_filtrado['Subarea'].isin(filtro_subarea)]  

        st.dataframe(  
            df_filtrado,  
            use_container_width=True,  
            hide_index=True  
        )  

    else:  # Estatísticas  
        st.header("Estatísticas de Progresso")  

        progresso = tracker.calcular_progresso_geral()  

        # Métricas principais  
        col1, col2, col3 = st.columns(3)  

        with col1:  
            st.metric(  
                "Progresso de Estudo",  
                f"{progresso['Progresso_Estudo']:.1f}%"  
            )  

        with col2:  
            st.metric(  
                "Progresso de Exercícios",  
                f"{progresso['Progresso_Exercicios']:.1f}%"  
            )  

        with col3:  
            st.metric(  
                "Média de Revisões",  
                f"{progresso['Media_Revisoes']:.1f}%"  
            )  

        # Gráficos  
        st.subheader("Progresso por Área")  
        relatorio = tracker.gerar_relatorio()  
        progresso_por_area = relatorio.groupby('Area').agg({  
            'Estudado': 'mean',  
            'Exercicios': 'mean',  
            'Revisao1': 'mean',  
            'Revisao2': 'mean',  
            'Revisao3': 'mean'  
        }) * 100  

        fig = px.bar(  
            progresso_por_area,  
            barmode='group',  
            title="Progresso por Área (%)"  
        )  
        st.plotly_chart(fig, use_container_width=True)  

if __name__ == "__main__":  
    main()  
