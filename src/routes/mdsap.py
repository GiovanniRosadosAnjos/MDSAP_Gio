from flask import Blueprint, request, jsonify
from src.models.mdsap_knowledge import db, MDSAPKnowledge, MDSAPGlossary, MDSAPCountry, AuditingOrganization
from sqlalchemy import or_

mdsap_bp = Blueprint('mdsap', __name__)

@mdsap_bp.route('/search', methods=['GET'])
def search_knowledge():
    """Busca no conhecimento MDSAP por palavra-chave ou tópico"""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    
    if not query and not category:
        return jsonify({'error': 'Parâmetro de busca (q) ou categoria é obrigatório'}), 400
    
    # Construir a consulta
    search_query = MDSAPKnowledge.query
    
    if query:
        search_query = search_query.filter(
            or_(
                MDSAPKnowledge.topic.contains(query),
                MDSAPKnowledge.content.contains(query),
                MDSAPKnowledge.keywords.contains(query)
            )
        )
    
    if category:
        search_query = search_query.filter(MDSAPKnowledge.category.ilike(f'%{category}%'))
    
    results = search_query.all()
    
    return jsonify({
        'results': [result.to_dict() for result in results],
        'total': len(results)
    })

@mdsap_bp.route('/glossary', methods=['GET'])
def get_glossary():
    """Retorna todos os termos do glossário MDSAP"""
    terms = MDSAPGlossary.query.order_by(MDSAPGlossary.term).all()
    return jsonify([term.to_dict() for term in terms])

@mdsap_bp.route('/glossary/<term>', methods=['GET'])
def get_glossary_term(term):
    """Busca um termo específico no glossário"""
    glossary_term = MDSAPGlossary.query.filter(
        or_(
            MDSAPGlossary.term.ilike(f'%{term}%'),
            MDSAPGlossary.acronym.ilike(f'%{term}%')
        )
    ).first()
    
    if not glossary_term:
        return jsonify({'error': 'Termo não encontrado'}), 404
    
    return jsonify(glossary_term.to_dict())

@mdsap_bp.route('/countries', methods=['GET'])
def get_countries():
    """Retorna informações sobre países participantes do MDSAP"""
    countries = MDSAPCountry.query.order_by(MDSAPCountry.country_name).all()
    return jsonify([country.to_dict() for country in countries])

@mdsap_bp.route('/countries/<country_name>', methods=['GET'])
def get_country_info(country_name):
    """Retorna informações específicas de um país"""
    country = MDSAPCountry.query.filter(
        MDSAPCountry.country_name.ilike(f'%{country_name}%')
    ).first()
    
    if not country:
        return jsonify({'error': 'País não encontrado'}), 404
    
    return jsonify(country.to_dict())

@mdsap_bp.route('/auditing-organizations', methods=['GET'])
def get_auditing_organizations():
    """Retorna lista de Organizações de Auditoria reconhecidas"""
    organizations = AuditingOrganization.query.filter_by(is_recognized=True).all()
    return jsonify([org.to_dict() for org in organizations])

@mdsap_bp.route('/categories', methods=['GET'])
def get_categories():
    """Retorna todas as categorias de conhecimento disponíveis"""
    categories = db.session.query(MDSAPKnowledge.category).distinct().all()
    return jsonify([category[0] for category in categories])

@mdsap_bp.route('/ask', methods=['POST'])
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
    
    # Palavras-chave para diferentes tipos de perguntas
    keywords_mapping = {
        'o que é': ['definição', 'conceito', 'introdução'],
        'como': ['processo', 'procedimento', 'etapas'],
        'quais': ['lista', 'tipos', 'categorias'],
        'onde': ['localização', 'países', 'jurisdições'],
        'quando': ['cronograma', 'prazo', 'tempo'],
        'por que': ['benefícios', 'objetivos', 'razões']
    }
    
    # Identificar o tipo de pergunta
    question_type = None
    for key in keywords_mapping:
        if key in question:
            question_type = key
            break
    
    # Buscar conhecimento relevante
    relevant_knowledge = []
    
    # Buscar por palavras-chave na pergunta
    words = question.split()
    for word in words:
        if len(word) > 3:  # Ignorar palavras muito curtas
            results = MDSAPKnowledge.query.filter(
                or_(
                    MDSAPKnowledge.topic.contains(word),
                    MDSAPKnowledge.content.contains(word),
                    MDSAPKnowledge.keywords.contains(word)
                )
            ).limit(5).all()
            relevant_knowledge.extend(results)
    
    # Remover duplicatas
    unique_knowledge = list({k.id: k for k in relevant_knowledge}.values())
    
    # Gerar resposta
    if not unique_knowledge:
        answer = "Desculpe, não encontrei informações específicas sobre sua pergunta. Você pode tentar reformular a pergunta ou buscar por termos mais específicos relacionados ao MDSAP."
        sources = []
        related_topics = []
    else:
        # Combinar conteúdo relevante
        content_parts = []
        sources = []
        related_topics = []
        
        for knowledge in unique_knowledge[:3]:  # Limitar a 3 resultados mais relevantes
            content_parts.append(knowledge.content)
            sources.append({
                'topic': knowledge.topic,
                'category': knowledge.category
            })
            if knowledge.topic not in related_topics:
                related_topics.append(knowledge.topic)
        
        answer = " ".join(content_parts)
        
        # Limitar o tamanho da resposta
        if len(answer) > 1000:
            answer = answer[:1000] + "..."
    
    return {
        'answer': answer,
        'sources': sources,
        'related_topics': related_topics[:5]  # Limitar a 5 tópicos relacionados
    }

