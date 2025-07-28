import os
import sys

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='../static')
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para todas as rotas
CORS(app)

# Dados em memória - Base de conhecimento MDSAP
KNOWLEDGE_DATA = [
    {
        'id': 1,
        'category': 'Introdução',
        'topic': 'O que é o MDSAP',
        'content': 'O Medical Device Single Audit Program (MDSAP) é uma iniciativa global que visa harmonizar os requisitos regulatórios para dispositivos médicos em diversos países. Reconhecido pelo Fórum Internacional de Reguladores de Produtos para Saúde (IMDRF), o MDSAP busca otimizar o processo de auditoria de fabricantes de dispositivos médicos, garantindo a segurança e a qualidade dos produtos em nível internacional.',
        'keywords': ['MDSAP', 'Medical Device Single Audit Program', 'IMDRF', 'auditoria', 'dispositivos médicos', 'harmonização']
    },
    {
        'id': 2,
        'category': 'Objetivos',
        'topic': 'Objetivos do MDSAP',
        'content': 'O principal objetivo do MDSAP é permitir que fabricantes de dispositivos médicos passem por uma única auditoria realizada por um Organismo Auditor (OA) reconhecido. Essa auditoria abrange os requisitos regulatórios de múltiplas jurisdições participantes, eliminando a necessidade de auditorias separadas por cada autoridade reguladora. Isso resulta em maior eficiência, redução de custos e minimização de interrupções nas operações de fabricação.',
        'keywords': ['objetivos', 'auditoria única', 'eficiência', 'redução de custos', 'Organismo Auditor', 'OA']
    },
    {
        'id': 3,
        'category': 'Países Participantes',
        'topic': 'Membros do MDSAP',
        'content': 'O MDSAP conta com a participação de cinco países membros principais: Austrália (TGA), Brasil (ANVISA), Canadá (Health Canada), Japão (MHLW e PMDA) e Estados Unidos (FDA). Além desses membros, o MDSAP possui países afiliados que utilizam os relatórios de auditoria para fins regulatórios, como Argentina, Indonésia, Israel, República da Coreia e Singapura.',
        'keywords': ['países membros', 'TGA', 'ANVISA', 'Health Canada', 'MHLW', 'PMDA', 'FDA', 'países afiliados']
    },
    {
        'id': 4,
        'category': 'Processo de Auditoria',
        'topic': 'Ciclo de Auditoria MDSAP',
        'content': 'O processo de auditoria MDSAP segue um ciclo de três anos, alinhado com os requisitos da ISO/IEC 17021. O ciclo compreende: Auditoria de Certificação Inicial (Estágio 1) - revisão da documentação; Auditoria de Certificação Inicial (Estágio 2) - avaliação aprofundada da conformidade; Auditorias de Vigilância - realizadas anualmente; e Auditoria de Recertificação - conduzida no terceiro ano.',
        'keywords': ['ciclo de auditoria', 'três anos', 'ISO/IEC 17021', 'estágio 1', 'estágio 2', 'vigilância', 'recertificação']
    },
    {
        'id': 5,
        'category': 'ISO 13485',
        'topic': 'Relação com ISO 13485',
        'content': 'A ISO 13485:2016 é a base fundamental do MDSAP. O certificado MDSAP não substitui a certificação ISO 13485, mas a complementa, incorporando os requisitos regulatórios dos países membros. No Canadá, a certificação MDSAP tornou-se obrigatória para a obtenção de licenças de dispositivos médicos de certas classes.',
        'keywords': ['ISO 13485', 'certificação', 'complementa', 'requisitos regulatórios', 'Canadá', 'obrigatória']
    },
    {
        'id': 6,
        'category': 'Benefícios',
        'topic': 'Benefícios do MDSAP',
        'content': 'Para os fabricantes de dispositivos médicos, o MDSAP oferece benefícios significativos: eficiência através da redução do número de auditorias; harmonização com conformidade a múltiplos requisitos regulatórios; facilitação do acesso a mercados internacionais; maior transparência e consistência na supervisão regulatória; e minimização das interrupções nas operações de fabricação.',
        'keywords': ['benefícios', 'eficiência', 'harmonização', 'acesso ao mercado', 'transparência', 'interrupções']
    },
    {
        'id': 7,
        'category': 'Documentos IMDRF',
        'topic': 'IMDRF/MDSAP WG/N4FINAL:2021 (Edition 2)',
        'content': 'O documento IMDRF/MDSAP WG/N4FINAL:2021 (Edition 2), intitulado "Competence and Training Requirements for Auditing Organizations", foi publicado em 16 de setembro de 2021 pelo IMDRF MDSAP Working Group. Ele estabelece os requisitos de competência e treinamento para Organizações de Auditoria reconhecidas que realizam auditorias em fabricantes de dispositivos médicos para fins regulatórios. O escopo abrange a garantia de que o pessoal da OA possua o compromisso, a competência, a experiência e o treinamento necessários para conduzir auditorias eficazes e consistentes. Detalha funções e papéis como Qualificador de Competência, Administrador de Programa, Auditor Líder/Auditor, Especialista Técnico e Revisor Final, com requisitos específicos para cada um.',
        'keywords': ['IMDRF', 'MDSAP', 'N4FINAL:2021', 'Competence', 'Training', 'Auditing Organizations', 'documento', 'requisitos', 'auditoria']
    }
]

# Glossário MDSAP
GLOSSARY_DATA = [
    {
        'id': 1,
        'term': 'Medical Device Single Audit Program',
        'acronym': 'MDSAP',
        'definition': 'Programa de Auditoria Única em Produtos para a Saúde, que permite uma única auditoria regulatória para múltiplos países.'
    },
    {
        'id': 2,
        'term': 'International Medical Device Regulators Forum',
        'acronym': 'IMDRF',
        'definition': 'Fórum Internacional de Reguladores de Produtos para Saúde, responsável pelo reconhecimento do MDSAP.'
    },
    {
        'id': 3,
        'term': 'Agência Nacional de Vigilância Sanitária',
        'acronym': 'ANVISA',
        'definition': 'Agência reguladora do Brasil, participante do MDSAP.'
    },
    {
        'id': 4,
        'term': 'Therapeutic Goods Administration',
        'acronym': 'TGA',
        'definition': 'Agência reguladora da Austrália, participante do MDSAP.'
    },
    {
        'id': 5,
        'term': 'U.S. Food and Drug Administration',
        'acronym': 'FDA',
        'definition': 'Agência reguladora dos Estados Unidos, participante do MDSAP.'
    },
    {
        'id': 6,
        'term': 'Organismo Auditor',
        'acronym': 'OA',
        'definition': 'Entidade autorizada pelo MDSAP para realizar auditorias em fabricantes de dispositivos médicos.'
    },
    {
        'id': 7,
        'term': 'Sistema de Gestão da Qualidade',
        'acronym': 'SGQ',
        'definition': 'Conjunto de processos e procedimentos que uma organização utiliza para garantir que seus produtos e serviços atendam aos requisitos do cliente e regulatórios.'
    },
    {
        'id': 8,
        'term': 'Electronic Product Radiation Control',
        'acronym': 'EPRC',
        'definition': 'Disposições de Controle de Radiação de Produtos Eletrônicos, para as quais a FDA ainda realiza inspeções separadas.'
    }
]

# Países participantes
COUNTRIES_DATA = [
    {
        'id': 1,
        'country_name': 'Austrália',
        'regulatory_agency': 'Therapeutic Goods Administration',
        'agency_acronym': 'TGA',
        'mdsap_usage': 'A TGA utiliza relatórios e certificados de auditoria MDSAP como parte da evidência avaliada para conformidade com os procedimentos de avaliação de conformidade de dispositivos médicos e requisitos de autorização de mercado.',
        'requirements': 'Conformidade com procedimentos de avaliação de conformidade e requisitos de autorização de mercado.',
        'is_member': True
    },
    {
        'id': 2,
        'country_name': 'Brasil',
        'regulatory_agency': 'Agência Nacional de Vigilância Sanitária',
        'agency_acronym': 'ANVISA',
        'mdsap_usage': 'A ANVISA utiliza relatórios de auditoria MDSAP em sua decisão de certificação para certificados GMP ANVISA brasileiros (a inspeção da ANVISA não é necessária).',
        'requirements': 'Certificados GMP ANVISA brasileiros.',
        'is_member': True
    },
    {
        'id': 3,
        'country_name': 'Canadá',
        'regulatory_agency': 'Health Canada',
        'agency_acronym': 'HC',
        'mdsap_usage': 'A certificação MDSAP é obrigatória para obter uma nova (ou manter ou alterar uma existente) licença de dispositivo médico Classe II, III ou IV.',
        'requirements': 'Certificação MDSAP obrigatória para dispositivos Classe II, III e IV.',
        'is_member': True
    },
    {
        'id': 4,
        'country_name': 'Japão',
        'regulatory_agency': 'Ministry of Health, Labour and Welfare / Pharmaceuticals and Medical Devices Agency',
        'agency_acronym': 'MHLW/PMDA',
        'mdsap_usage': 'Utilizam os relatórios MDSAP para isentar locais de fabricação de inspeções no local e/ou permitir que um detentor de autorização de comercialização substitua uma parte considerável dos documentos exigidos para a inspeção pelo relatório.',
        'requirements': 'Inspeções QMS pré-mercado ou pós-mercado periódicas.',
        'is_member': True
    },
    {
        'id': 5,
        'country_name': 'Estados Unidos',
        'regulatory_agency': 'U.S. Food and Drug Administration',
        'agency_acronym': 'FDA',
        'mdsap_usage': 'O Centro de Dispositivos e Saúde Radiológica (CDRH) da FDA aceita os relatórios de auditoria MDSAP como um substituto para as inspeções de rotina da FDA.',
        'requirements': 'Empresas com atividades EPRC continuam sujeitas a inspeções da FDA.',
        'is_member': True
    }
]

# Organizações de Auditoria
AUDITING_ORGS_DATA = [
    {
        'id': 1,
        'name': 'BSI Group America Inc.',
        'location': 'Herndon, VA, USA',
        'contact_person': 'Morgan Quandt',
        'contact_email': 'Morgan.quandt@bsigroup.com',
        'contact_phone': '+1 571 443 1708',
        'is_recognized': True,
        'website': 'https://www.bsigroup.com'
    },
    {
        'id': 2,
        'name': 'DEKRA Certification B.V.',
        'location': 'Arnhem, Netherlands',
        'contact_person': 'Adriano Mulloni',
        'contact_email': 'mdsap.nl@dekra.com',
        'contact_phone': '+31 88 96 83000',
        'is_recognized': True,
        'website': 'https://www.dekra.com'
    },
    {
        'id': 3,
        'name': 'DNV Product Assurance AS',
        'location': 'Hovik, Norway',
        'contact_person': 'Zaher Kharboutly',
        'contact_email': 'zaher.kharboutly@dnv.com',
        'contact_phone': '+1 416 276 9525',
        'is_recognized': True,
        'website': 'https://www.dnv.com'
    },
    {
        'id': 4,
        'name': 'UL LLC, UL Solutions medical regulatory services',
        'location': 'Northbrook, IL, USA',
        'contact_person': 'Chiranjit Deka',
        'contact_email': 'chiranjit.deka@ul.com',
        'contact_phone': '+1 919-208-4704',
        'is_recognized': True,
        'website': 'https://www.ul.com'
    },
    {
        'id': 5,
        'name': 'TÜV SÜD America Inc.',
        'location': 'Wakefield, MA, USA',
        'contact_person': 'Dawn Tibodeau',
        'contact_email': 'Dawn.Tibodeau@tuvsud.com',
        'contact_phone': '+1 651 638 0288',
        'is_recognized': True,
        'website': 'https://www.tuvsud.com'
    }
]

@app.route('/api/mdsap/search', methods=['GET'])
def search_knowledge():
    """Busca no conhecimento MDSAP por palavra-chave ou tópico"""
    query = request.args.get('q', '').strip().lower()
    category = request.args.get('category', '').strip().lower()
    
    if not query and not category:
        return jsonify({'error': 'Parâmetro de busca (q) ou categoria é obrigatório'}), 400
    
    results = []
    
    for knowledge in KNOWLEDGE_DATA:
        match = False
        
        if query:
            # Buscar na topic, content e keywords
            if (query in knowledge['topic'].lower() or 
                query in knowledge['content'].lower() or 
                any(query in keyword.lower() for keyword in knowledge['keywords'])):
                match = True
        
        if category:
            if category in knowledge['category'].lower():
                match = True
        
        if match:
            results.append({
                'id': knowledge['id'],
                'category': knowledge['category'],
                'topic': knowledge['topic'],
                'content': knowledge['content'],
                'keywords': knowledge['keywords']
            })
    
    return jsonify({
        'results': results,
        'total': len(results)
    })

@app.route('/api/mdsap/glossary', methods=['GET'])
def get_glossary():
    """Retorna todos os termos do glossário MDSAP"""
    return jsonify([{
        'id': term['id'],
        'term': term['term'],
        'definition': term['definition'],
        'acronym': term['acronym']
    } for term in GLOSSARY_DATA])

@app.route('/api/mdsap/glossary/<term>', methods=['GET'])
def get_glossary_term(term):
    """Busca um termo específico no glossário"""
    term_lower = term.lower()
    
    for glossary_term in GLOSSARY_DATA:
        if (term_lower in glossary_term['term'].lower() or 
            (glossary_term['acronym'] and term_lower in glossary_term['acronym'].lower())):
            return jsonify({
                'id': glossary_term['id'],
                'term': glossary_term['term'],
                'definition': glossary_term['definition'],
                'acronym': glossary_term['acronym']
            })
    
    return jsonify({'error': 'Termo não encontrado'}), 404

@app.route('/api/mdsap/countries', methods=['GET'])
def get_countries():
    """Retorna informações sobre países participantes do MDSAP"""
    return jsonify([{
        'id': country['id'],
        'country_name': country['country_name'],
        'regulatory_agency': country['regulatory_agency'],
        'agency_acronym': country['agency_acronym'],
        'mdsap_usage': country['mdsap_usage'],
        'requirements': country['requirements'],
        'is_member': country['is_member']
    } for country in COUNTRIES_DATA])

@app.route('/api/mdsap/countries/<country_name>', methods=['GET'])
def get_country_info(country_name):
    """Retorna informações específicas de um país"""
    country_name_lower = country_name.lower()
    
    for country in COUNTRIES_DATA:
        if country_name_lower in country['country_name'].lower():
            return jsonify({
                'id': country['id'],
                'country_name': country['country_name'],
                'regulatory_agency': country['regulatory_agency'],
                'agency_acronym': country['agency_acronym'],
                'mdsap_usage': country['mdsap_usage'],
                'requirements': country['requirements'],
                'is_member': country['is_member']
            })
    
    return jsonify({'error': 'País não encontrado'}), 404

@app.route('/api/mdsap/auditing-organizations', methods=['GET'])
def get_auditing_organizations():
    """Retorna lista de Organizações de Auditoria reconhecidas"""
    return jsonify([{
        'id': org['id'],
        'name': org['name'],
        'location': org['location'],
        'contact_person': org['contact_person'],
        'contact_email': org['contact_email'],
        'contact_phone': org['contact_phone'],
        'is_recognized': org['is_recognized'],
        'website': org['website']
    } for org in AUDITING_ORGS_DATA if org['is_recognized']])

@app.route('/api/mdsap/categories', methods=['GET'])
def get_categories():
    """Retorna todas as categorias de conhecimento disponíveis"""
    categories = list(set(knowledge['category'] for knowledge in KNOWLEDGE_DATA))
    return jsonify(categories)

@app.route('/api/mdsap/ask', methods=['POST'])
def ask_question():
    """Endpoint principal para fazer perguntas ao agente MDSAP"""
    data = request.get_json()
    
    if not data or 'question' not in data:
        return jsonify({'error': 'Pergunta é obrigatória'}), 400
    
    question = data['question'].strip().lower()
    
    # Lógica simples de processamento de perguntas
    response = process_question(question)
    
    return jsonify({
        'question': data['question'],
        'answer': response['answer'],
        'sources': response['sources'],
        'related_topics': response['related_topics']
    })

def process_question(question):
    """Processa a pergunta e retorna uma resposta baseada no conhecimento"""
    
    # Buscar conhecimento relevante
    relevant_knowledge = []
    
    # Buscar por palavras-chave na pergunta
    words = question.split()
    for word in words:
        if len(word) > 3:  # Ignorar palavras muito curtas
            for knowledge in KNOWLEDGE_DATA:
                if (word in knowledge['topic'].lower() or 
                    word in knowledge['content'].lower() or 
                    any(word in keyword.lower() for keyword in knowledge['keywords'])):
                    if knowledge not in relevant_knowledge:
                        relevant_knowledge.append(knowledge)
    
    # Gerar resposta
    if not relevant_knowledge:
        answer = "Desculpe, não encontrei informações específicas sobre sua pergunta. Você pode tentar reformular a pergunta ou buscar por termos mais específicos relacionados ao MDSAP."
        sources = []
        related_topics = []
    else:
        # Combinar conteúdo relevante
        content_parts = []
        sources = []
        related_topics = []
        
        for knowledge in relevant_knowledge[:3]:  # Limitar a 3 resultados mais relevantes
            content_parts.append(f"**{knowledge['topic']}**: {knowledge['content']}")
            sources.append(knowledge['category'])
            related_topics.append(knowledge['topic'])
        
        answer = "\n".join(content_parts)
        
        # Adicionar uma resposta padrão se a busca for muito ampla
        if len(relevant_knowledge) > 3:
            answer += "\n\nEncontrei mais informações relevantes. Por favor, seja mais específico em sua pergunta para obter uma resposta mais detalhada."

    return {
        'answer': answer,
        'sources': list(set(sources)),  # Remover duplicatas
        'related_topics': list(set(related_topics)) # Remover duplicatas
    }

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return send_from_directory(app.static_folder, 'index.html')

# Para Vercel
# A variável `app` é o WSGI callable que o Vercel espera.
# Não é necessário um `if __name__ == '__main__'` para o deploy no Vercel.
# O Vercel irá importar `app` diretamente.

