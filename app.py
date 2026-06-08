import streamlit as st
from openai import OpenAI

# Configuração visual do site
st.set_page_config(page_title="AnamneMed AI", page_icon="🩺", layout="wide")

# Agora o código procura a chave no cofre digital seguro da nuvem
API_KEY = st.secrets["OPENAI_API_KEY"]

st.title("🩺 AnamneMed")
st.subheader("Transforme anotações soltas em anamneses estruturadas instantaneamente")
st.markdown("---")
# ========================================================
# 📲 COMPONENTE DA BARRA LATERAL (SIDEBAR INSTITUCIONAL)
# ========================================================
with st.sidebar:
    st.title("🩺 AnamneMed AI")
    st.subheader("Sua assistente de produtividade clínica")
    st.markdown("---")
    
    # 🛡️ Blindagem Jurídica e Aviso Legal
    st.markdown("### 🛡️ Aviso Legal")
    st.info(
        "O AnamneMed AI é uma ferramenta exclusiva de suporte à documentação e digitação clínica. "
        "A Inteligência Artificial não emite diagnósticos, não prescreve tratamentos e não substitui o julgamento médico. "
        "A revisão, validação e assinatura final do documento gerado são de responsabilidade 100% exclusiva do médico responsável."
    )
    
    st.markdown("---")
    st.markdown("⚙️ **Plataforma:** Versão 1.0 (MVP)")
    st.markdown("🚀 *Desenvolvido para Médicos e Acadêmicos*")
    st.markdown("💬 [Suporte & Feedback](mailto:suporte@anamnedmed.com)")
# ========================================================
# Dividindo a tela ao meio
col1, col2 = st.columns(2)

with col1:
    st.subheader("✍️ Anotações do Médico")
    texto_baguncado = st.text_area(
        "Insira as informações da consulta:",
        placeholder="Ex: Winicius Jr, dor de cabeça do lado direito, tem 2 dias sem parar...",
        height=300
    )
    botao_estruturar = st.button("🚀 Estruturar Anamnese", use_container_width=True)

with col2:
    st.subheader("📋 Anamnese Estruturada")
    
    if botao_estruturar:
        if texto_baguncado.strip() == "":
            st.warning("Por favor, digite alguma informação antes de estruturar!")
        elif API_KEY == "SUA_CHAVE_AQUI":
            st.error("Atenção: Você precisa colar a sua chave secreta da OpenAI na linha 7 do código!")
        else:
            with st.spinner("A Inteligência Artificial está organizando os dados médicos..."):
                try:
                    client = OpenAI(api_key=API_KEY)
                    
                    # ENGENHARIA DE PROMPT ATUALIZADA COM SUAS REGRAS CIRÚRGICAS:
                    PROMPT_MEDICO = """
                    Você é um assistente médico de alta precisão especializado em estruturar anamneses profissionais.
                    Sua tarefa é receber um texto clínico confuso, bagunçado ou ditado e organizá-lo rigorosamente no padrão formal, seguindo as regras abaixo:

                    Estruture o documento estritamente nas seguintes seções:
                    1. **Identificação do Paciente:** Inclua nome completo, idade, data de nascimento, estado civil, sexo, gênero, raça/cor, profissão atual e ocupações anteriores, naturalidade, procedência, nome da mãe e nome do acompanhante. Se alguma dessas informações não for mencionada, simplesmente omita a informação, não coloque os tópicos mesmo com "não mencionado" ou "desconhecido", deixe-os de fora completamente.
                    *REGRA CRUCIAL DE OMISSÃO:* É terminantemente PROIBIDO escrever termos como "não mencionado", "não indicado", "desconhecido", "não informado", "não declarado" ou usar placeholders para dados ausentes na "Identificação do Paciente". Se uma informação de identificação não foi dita pelo médico, simplesmente oculte-a. Ela não deve aparecer na tela de forma alguma.
                    2. **Queixa Principal (QP):** Apresente o motivo da consulta utilizando EXATAMENTE as palavras leigas ditas pelo paciente (ex: "dor de cabeça", "batedeira no peito", "estrelinhas na visão"). Não mude os termos aqui. Coloque também a duração do sintoma, se mencionada (ex: "dor de cabeça há 2 dias").
                    3. **História da Doença Atual (HDA):** Traduza todos os termos leigos para a terminologia médica formal (ex: "dor de cabeça" vira "cefaleia", "falta de ar" vira "dispneia", "ver estrelinhas" vira "escotomas cintilantes"). Esta seção deve ser escrita OBRIGATORIAMENTE em TEXTO CORRIDO (narrativa contínua em parágrafos), NUNCA em tópicos ou bullet points.
                    4. **Sintomas Associados e Revisão de Sistemas:** Liste os outros sintomas relatados ou negados pertinentes.
                    5. **Interrogatório Sintomatológico:** Organize os sintomas em sistemas (ex: Sintomas Gerais, Pele e Fâneros, Cabeça e Pescoço, Aparelho Respiratório, Aparelho Cardiovasvular, Aparelho Digestivo, Aparelho Geniturinário, Sistema Osteoarticular e Muscular, Sistema Nervoso, Sistema Endócrino, Sistema Hemolinfopoético) você deve identificar os sintomas e organizá-los de acordo com o sistema afetado, utilizando os termos médicos corretos. se não apresentar sintomas relacionados a um sistema, deixe o título do sistema e escreva "Negado", priorize e deixe os sistemas que tiverem sintomas na frente, e os sistemas sem sintomas no final.)
                    6. **Antecedentes (Pessoais, Fisiológicos, Patológicos e Familiares):** Organiza o histórico médico, hábitos e patologias prévias do paciente ou da família. OBRIGATORIAMENTE use o formato de TÓPICOS (bullet points) para subdividir as informações encontradas. Utilize termos médicos para se referir a doenças, condições e hábitos (ex: "diabetes mellitus tipo 2" ao invés de "diabetes", "hipertensão arterial sistêmica" ao invés de "pressão alta" ou "HAS", "tabagismo" ao invés de "fuma", "etilismo" ao invés de "bebe"). 
                       *REGRA CRUCIAL DE OMISSÃO:* Se o médico não tiver mencionado absolutamente nenhuma informação sobre antecedentes (sejam familiares, pessoais ou patologias passadas), NÃO exiba esta seção de forma alguma. O título e os tópicos devem sumir completamente do resultado final.
                    7. **Termos não compreendidos:** Toda informação mencionada é de extremo valor e importância, mesmo que seja confusa ou difícil de entender. Se houver termos ou expressões que não estejam claras ou que sejam ambíguas, liste-os em uma seção separada chamada "Termos Não Compreendidos". Nessa seção, escreva exatamente o que foi dito, sem tentar adivinhar ou interpretar. Toda e qualquer informação que você não conseguir encaixar na anamnese deve ser listada aqui, para que o médico possa revisar e esclarecer posteriormente. Se não houver termos confusos ou não compreendidos, simplesmente omita essa seção do resultado final, sem deixar títulos ou placeholders vazios.
                    8. **💡 Sugestões de Conduta:** No final, crie uma seção curta com 3 perguntas clínicas inteligentes que o médico poderia fazer para complementar a investigação.

                    Regras Cruciais:
                    - Nunca invente dados, sintomas ou diagnósticos que não foram citados no texto do usuário.
                    - Se uma seção opcional (como a de Antecedentes) não tiver dados correspondentes no texto inserido, oculte-a totalmente do resultado final. Não crie placeholders ou títulos vazios.
                    - Mantenha a precisão técnica impecável nas traduções de termos.
                    - O resultado final deve ser um documento médico profissional, claro, organizado e pronto para ser adicionado ao prontuário do paciente.
                    """
                    
                    resposta = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": PROMPT_MEDICO},
                            {"role": "user", "content": texto_baguncado}
                        ]
                    )
                    
                    resultado_real = resposta.choices[0].message.content
                    resultado_real = resposta.choices[0].message.content
                    
                    # 📋 EXIBIÇÃO COM BOTÃO DE COPIAR NATIVO
                    st.markdown("### 📄 Texto Pronto:")
                    st.code(resultado_real, language="markdown")
                    st.success("Pronto! Clique no ícone que fica no canto superior direito da caixa preta acima para copiar.")
                    
                except Exception as e:
                    st.error(f"Ops, ocorreu um erro ao falar com a IA: {e}")
    else:
        st.write("As informações organizadas pela IA aparecerão aqui assim que você clicar no botão ao lado.")