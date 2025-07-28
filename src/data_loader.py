import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.mdsap_knowledge import db, MDSAPKnowledge, MDSAPGlossary, MDSAPCountry, AuditingOrganization
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def load_knowledge_data():
    """Carrega dados de conhecimento MDSAP"""
    
    knowledge_data = [
        {
            'category': 'Introdução',
            'topic': 'O que é o MDSAP',
            'content': 'O Medical Device Single Audit Program (MDSAP) é uma iniciativa global que visa harmonizar os requisitos regulatórios para dispositivos médicos em diversos países. Reconhecido pelo Fórum Internacional de Reguladores de Produtos para Saúde (IMDRF), o MDSAP busca otimizar o processo de auditoria de fabricantes de dispositivos médicos, garantindo a segurança e a qualidade dos produtos em nível internacional.',
            'keywords': 'MDSAP,Medical Device Single Audit Program,IMDRF,auditoria,dispositivos médicos,harmonização'
        },
        {
            'category': 'Objetivos',
            'topic': 'Objetivos do MDSAP',
            'content': 'O principal objetivo do MDSAP é permitir que fabricantes de dispositivos médicos passem por uma única auditoria realizada por um Organismo Auditor (OA) reconhecido. Essa auditoria abrange os requisitos regulatórios de múltiplas jurisdições participantes, eliminando a necessidade de auditorias separadas por cada autoridade reguladora. Isso resulta em maior eficiência, redução de custos e minimização de interrupções nas operações de fabricação.',
            'keywords': 'objetivos,auditoria única,eficiência,redução de custos,Organismo Auditor,OA'
        },
        {
            'category': 'Países Participantes',
            'topic': 'Membros do MDSAP',
            'content': 'O MDSAP conta com a participação de cinco países membros principais: Austrália (TGA), Brasil (ANVISA), Canadá (Health Canada), Japão (MHLW e PMDA) e Estados Unidos (FDA). Além desses membros, o MDSAP possui países afiliados que utilizam os relatórios de auditoria para fins regulatórios, como Argentina, Indonésia, Israel, República da Coreia e Singapura.',
            'keywords': 'países membros,TGA,ANVISA,Health Canada,MHLW,PMDA,FDA,países afiliados'
        },
        {
            'category': 'Processo de Auditoria',
            'topic': 'Ciclo de Auditoria MDSAP',
            'content': 'O processo de auditoria MDSAP segue um ciclo de três anos, alinhado com os requisitos da ISO/IEC 17021. O ciclo compreende: Auditoria de Certificação Inicial (Estágio 1) - revisão da documentação; Auditoria de Certificação Inicial (Estágio 2) - avaliação aprofundada da conformidade; Auditorias de Vigilância - realizadas anualmente; e Auditoria de Recertificação - conduzida no terceiro ano.',
            'keywords': 'ciclo de auditoria,três anos,ISO/IEC 17021,estágio 1,estágio 2,vigilância,recertificação'
        },
        {
            'category': 'ISO 13485',
            'topic': 'Relação com ISO 13485',
            'content': 'A ISO 13485:2016 é a base fundamental do MDSAP. O certificado MDSAP não substitui a certificação ISO 13485, mas a complementa, incorporando os requisitos regulatórios dos países membros. No Canadá, a certificação MDSAP tornou-se obrigatória para a obtenção de licenças de dispositivos médicos de certas classes.',
            'keywords': 'ISO 13485,certificação,complementa,requisitos regulatórios,Canadá,obrigatória'
        },
        {
            'category': 'Benefícios',
            'topic': 'Benefícios do MDSAP',
            'content': 'Para os fabricantes de dispositivos médicos, o MDSAP oferece benefícios significativos: eficiência através da redução do número de auditorias; harmonização com conformidade a múltiplos requisitos regulatórios; facilitação do acesso a mercados internacionais; maior transparência e consistência na supervisão regulatória; e minimização das interrupções nas operações de fabricação.',
            'keywords': 'benefícios,eficiência,harmonização,acesso ao mercado,transparência,interrupções'
        }
    ]
    
    for data in knowledge_data:
        knowledge = MDSAPKnowledge(
            category=data['category'],
            topic=data['topic'],
            content=data['content'],
            keywords=data['keywords']
        )
        db.session.add(knowledge)

def load_glossary_data():
    """Carrega dados do glossário MDSAP"""
    
    glossary_data = [
        {
            'term': 'Medical Device Single Audit Program',
            'acronym': 'MDSAP',
            'definition': 'Programa de Auditoria Única em Produtos para a Saúde, que permite uma única auditoria regulatória para múltiplos países.'
        },
        {
            'term': 'International Medical Device Regulators Forum',
            'acronym': 'IMDRF',
            'definition': 'Fórum Internacional de Reguladores de Produtos para Saúde, responsável pelo reconhecimento do MDSAP.'
        },
        {
            'term': 'Agência Nacional de Vigilância Sanitária',
            'acronym': 'ANVISA',
            'definition': 'Agência reguladora do Brasil, participante do MDSAP.'
        },
        {
            'term': 'Therapeutic Goods Administration',
            'acronym': 'TGA',
            'definition': 'Agência reguladora da Austrália, participante do MDSAP.'
        },
        {
            'term': 'U.S. Food and Drug Administration',
            'acronym': 'FDA',
            'definition': 'Agência reguladora dos Estados Unidos, participante do MDSAP.'
        },
        {
            'term': 'Organismo Auditor',
            'acronym': 'OA',
            'definition': 'Entidade autorizada pelo MDSAP para realizar auditorias em fabricantes de dispositivos médicos.'
        },
        {
            'term': 'Sistema de Gestão da Qualidade',
            'acronym': 'SGQ',
            'definition': 'Conjunto de processos e procedimentos que uma organização utiliza para garantir que seus produtos e serviços atendam aos requisitos do cliente e regulatórios.'
        },
        {
            'term': 'Electronic Product Radiation Control',
            'acronym': 'EPRC',
            'definition': 'Disposições de Controle de Radiação de Produtos Eletrônicos, para as quais a FDA ainda realiza inspeções separadas.'
        }
    ]
    
    for data in glossary_data:
        term = MDSAPGlossary(
            term=data['term'],
            acronym=data['acronym'],
            definition=data['definition']
        )
        db.session.add(term)

def load_countries_data():
    """Carrega dados dos países participantes"""
    
    countries_data = [
        {
            'country_name': 'Austrália',
            'regulatory_agency': 'Therapeutic Goods Administration',
            'agency_acronym': 'TGA',
            'mdsap_usage': 'A TGA utiliza relatórios e certificados de auditoria MDSAP como parte da evidência avaliada para conformidade com os procedimentos de avaliação de conformidade de dispositivos médicos e requisitos de autorização de mercado.',
            'requirements': 'Conformidade com procedimentos de avaliação de conformidade e requisitos de autorização de mercado.',
            'is_member': True
        },
        {
            'country_name': 'Brasil',
            'regulatory_agency': 'Agência Nacional de Vigilância Sanitária',
            'agency_acronym': 'ANVISA',
            'mdsap_usage': 'A ANVISA utiliza relatórios de auditoria MDSAP em sua decisão de certificação para certificados GMP ANVISA brasileiros (a inspeção da ANVISA não é necessária).',
            'requirements': 'Certificados GMP ANVISA brasileiros.',
            'is_member': True
        },
        {
            'country_name': 'Canadá',
            'regulatory_agency': 'Health Canada',
            'agency_acronym': 'HC',
            'mdsap_usage': 'A certificação MDSAP é obrigatória para obter uma nova (ou manter ou alterar uma existente) licença de dispositivo médico Classe II, III ou IV.',
            'requirements': 'Certificação MDSAP obrigatória para dispositivos Classe II, III e IV.',
            'is_member': True
        },
        {
            'country_name': 'Japão',
            'regulatory_agency': 'Ministry of Health, Labour and Welfare / Pharmaceuticals and Medical Devices Agency',
            'agency_acronym': 'MHLW/PMDA',
            'mdsap_usage': 'Utilizam os relatórios MDSAP para isentar locais de fabricação de inspeções no local e/ou permitir que um detentor de autorização de comercialização substitua uma parte considerável dos documentos exigidos para a inspeção pelo relatório.',
            'requirements': 'Inspeções QMS pré-mercado ou pós-mercado periódicas.',
            'is_member': True
        },
        {
            'country_name': 'Estados Unidos',
            'regulatory_agency': 'U.S. Food and Drug Administration',
            'agency_acronym': 'FDA',
            'mdsap_usage': 'O Centro de Dispositivos e Saúde Radiológica (CDRH) da FDA aceita os relatórios de auditoria MDSAP como um substituto para as inspeções de rotina da FDA.',
            'requirements': 'Empresas com atividades EPRC continuam sujeitas a inspeções da FDA.',
            'is_member': True
        }
    ]
    
    for data in countries_data:
        country = MDSAPCountry(
            country_name=data['country_name'],
            regulatory_agency=data['regulatory_agency'],
            agency_acronym=data['agency_acronym'],
            mdsap_usage=data['mdsap_usage'],
            requirements=data['requirements'],
            is_member=data['is_member']
        )
        db.session.add(country)

def load_auditing_organizations_data():
    """Carrega dados das Organizações de Auditoria"""
    
    organizations_data = [
        {
            'name': 'BSI Group America Inc.',
            'location': 'Herndon, VA, USA',
            'contact_person': 'Morgan Quandt',
            'contact_email': 'Morgan.quandt@bsigroup.com',
            'contact_phone': '+1 571 443 1708',
            'is_recognized': True,
            'website': 'https://www.bsigroup.com'
        },
        {
            'name': 'DEKRA Certification B.V.',
            'location': 'Arnhem, Netherlands',
            'contact_person': 'Adriano Mulloni',
            'contact_email': 'mdsap.nl@dekra.com',
            'contact_phone': '+31 88 96 83000',
            'is_recognized': True,
            'website': 'https://www.dekra.com'
        },
        {
            'name': 'DNV Product Assurance AS',
            'location': 'Hovik, Norway',
            'contact_person': 'Zaher Kharboutly',
            'contact_email': 'zaher.kharboutly@dnv.com',
            'contact_phone': '+1 416 276 9525',
            'is_recognized': True,
            'website': 'https://www.dnv.com'
        },
        {
            'name': 'UL LLC, UL Solutions medical regulatory services',
            'location': 'Northbrook, IL, USA',
            'contact_person': 'Chiranjit Deka',
            'contact_email': 'chiranjit.deka@ul.com',
            'contact_phone': '+1 919-208-4704',
            'is_recognized': True,
            'website': 'https://www.ul.com'
        },
        {
            'name': 'TÜV SÜD America Inc.',
            'location': 'Wakefield, MA, USA',
            'contact_person': 'Dawn Tibodeau',
            'contact_email': 'Dawn.Tibodeau@tuvsud.com',
            'contact_phone': '+1 651 638 0288',
            'is_recognized': True,
            'website': 'https://www.tuvsud.com'
        }
    ]
    
    for data in organizations_data:
        org = AuditingOrganization(
            name=data['name'],
            location=data['location'],
            contact_person=data['contact_person'],
            contact_email=data['contact_email'],
            contact_phone=data['contact_phone'],
            is_recognized=data['is_recognized'],
            website=data['website']
        )
        db.session.add(org)

def main():
    app = create_app()
    
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar se os dados já foram carregados
        if MDSAPKnowledge.query.count() == 0:
            print("Carregando dados de conhecimento...")
            load_knowledge_data()
        
        if MDSAPGlossary.query.count() == 0:
            print("Carregando dados do glossário...")
            load_glossary_data()
        
        if MDSAPCountry.query.count() == 0:
            print("Carregando dados dos países...")
            load_countries_data()
        
        if AuditingOrganization.query.count() == 0:
            print("Carregando dados das organizações de auditoria...")
            load_auditing_organizations_data()
        
        # Salvar todas as alterações
        db.session.commit()
        print("Dados carregados com sucesso!")

if __name__ == '__main__':
    main()

