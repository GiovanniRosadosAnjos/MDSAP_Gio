from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MDSAPKnowledge(db.Model):
    __tablename__ = 'mdsap_knowledge'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.Text)  # Palavras-chave separadas por vírgula
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'topic': self.topic,
            'content': self.content,
            'keywords': self.keywords.split(',') if self.keywords else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class MDSAPGlossary(db.Model):
    __tablename__ = 'mdsap_glossary'
    
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), nullable=False, unique=True)
    definition = db.Column(db.Text, nullable=False)
    acronym = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'term': self.term,
            'definition': self.definition,
            'acronym': self.acronym,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class MDSAPCountry(db.Model):
    __tablename__ = 'mdsap_countries'
    
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(100), nullable=False)
    regulatory_agency = db.Column(db.String(200), nullable=False)
    agency_acronym = db.Column(db.String(20))
    mdsap_usage = db.Column(db.Text)  # Como o país utiliza o MDSAP
    requirements = db.Column(db.Text)  # Requisitos específicos do país
    is_member = db.Column(db.Boolean, default=True)  # True para membros, False para afiliados
    
    def to_dict(self):
        return {
            'id': self.id,
            'country_name': self.country_name,
            'regulatory_agency': self.regulatory_agency,
            'agency_acronym': self.agency_acronym,
            'mdsap_usage': self.mdsap_usage,
            'requirements': self.requirements,
            'is_member': self.is_member
        }

class AuditingOrganization(db.Model):
    __tablename__ = 'auditing_organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    contact_person = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(50))
    is_recognized = db.Column(db.Boolean, default=True)
    website = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'contact_person': self.contact_person,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'is_recognized': self.is_recognized,
            'website': self.website
        }

