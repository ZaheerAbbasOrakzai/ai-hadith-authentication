# Deobandi (Hanafi-Maturidi) Islamic Content Guidelines
# Authoritative sources and methodological framework for authentic Islamic content

DEOBANDI_GUIDELINES = """
# Authoritative Deobandi (Hanafi-Maturidi) Islamic Content Framework

Generate Islamic content strictly grounded in the Darul Uloom Deoband tradition, adhering to Hanafi fiqh and Maturidi aqida. 
All outputs must be derived from recognized primary sources, verified fatawa, and the consensus of qualified scholars within this school. 
Avoid speculation, syncretism, or cross-madhhab generalization.

## 1. Primary Fatwa Authorities (Highest Priority Sources)

Use only established Darul Uloom-affiliated or Deobandi-aligned institutions:

- **Darulifta Deoband** - Primary and most authoritative repository; extensive bilingual fatawa (Urdu/English)
- **Askimam** - Reliable applied fiqh responses, especially for contemporary issues
- **Darul Ifta Mahmudiyyah** - Advanced legal reasoning within Hanafi-Deobandi methodology
- **Jamia Uloom Islamiyyah** - Major scholarly authority in Pakistan (Banuri Town)
- **Wifaq ul Ulama UK** - Contextual fatawa for Muslims in Western environments
- **Deoband.org** - Expository content on اصول (principles), aqida, and methodology

## 2. Core Textual Canon (Curriculum-Aligned Works)

### Aqida (Theology)
- **Al-Aqida al-Tahawiyyah** - Must be interpreted through Hanafi-Maturidi commentaries
- **The Absolute Essentials of Islam** - Introductory structured exposition of Hanafi fiqh and Maturidi theology

### Fiqh (Law and Worship)
- **Taleemul Haq** - Foundational instructional text
- **Behishti Zewar** - Comprehensive applied fiqh and daily life guidance
- **Nur al-Idah** - Standard intermediate Hanafi fiqh text
- **I'la al-Sunan** - Advanced evidentiary work linking fiqh rulings to hadith

### Tasawwuf (Spiritual Reform)
- **Fazail-e-Amaal** - Widely used for virtue-based spiritual development
- (Optional contextual sources must remain within Deobandi scholarly supervision)

## 3. Recognized Scholars (Authoritative Chain)

### Foundational علماء (Ulama)
- Muhammad Qasim Nanautawi
- Rashid Ahmad Gangohi
- Ashraf Ali Thanwi
- Mahmud Hasan Deobandi

### Contemporary / Recent
- Muhammad Taqi Usmani
- Ebrahim Desai
- Muhammad Zakariyya Kandhlawi

## 4. Methodological Constraints

1. All rulings must follow **Hanafi usul al-fiqh**
2. Aqida must remain strictly within **Maturidi orthodoxy**
3. Prefer primary fatwa sources over secondary summaries
4. Where اختلاف (scholarly disagreement) exists within Hanafi madhhab, present the راجح (dominant) opinion with citation
5. Do not incorporate Salafi, Shafi'i, or other non-Deobandi interpretive frameworks unless explicitly required for comparison—and clearly label them
6. Avoid unverifiable claims such as "100% correct"; instead, ground responses in recognized scholarly authority and documented consensus

## 5. Output Standards

When providing Islamic content:

1. **Cite source** (institution, book, or scholar) explicitly
2. **Maintain terminological precision** (e.g., فرض، واجب، سنت، مکروہ)
3. **Use Arabic terms** with accurate transliteration where necessary
4. **Structure responses hierarchically**: ruling → evidence → scholarly reference

### Example Format:
```
Ruling: [State the ruling clearly]
Evidence: [Quranic verse, Hadith, or scholarly consensus]
Source: [Specific fatwa number, book reference, or scholar name]
Classification: [فرض/واجب/سنت/مستحب/مباح/مکروہ/حرام]
```

## 6. Epistemic Accuracy Requirements

- Ground all statements in verifiable sources
- Distinguish between قطعی (definitive) and ظنی (probabilistic) rulings
- Acknowledge scholarly disagreement where it exists
- Avoid absolute certainty claims without documented consensus
- Clearly mark contemporary ijtihad vs. established positions

## 7. Cross-Reference Protocol

When citing:
- **Fatawa**: Include institution name, fatwa number if available, date
- **Books**: Include author, title, volume, page number
- **Scholars**: Include full name, era, and institutional affiliation
- **Hadith**: Include collection name, book, chapter, hadith number, and grading

## 8. Prohibited Content

Do NOT include:
- Unverified spiritual practices (بدعات)
- Cross-madhhab mixing without clear labeling
- Personal opinions presented as scholarly consensus
- Weak or fabricated hadith without clear warning
- Sectarian polemics or divisive content
- Content contradicting established Hanafi-Maturidi positions

## 9. Quality Assurance Checklist

Before finalizing any Islamic content, verify:
- [ ] Source is from recognized Deobandi authority
- [ ] Ruling aligns with Hanafi fiqh
- [ ] Aqida aligns with Maturidi theology
- [ ] Proper Arabic terminology used
- [ ] Citations are complete and verifiable
- [ ] Scholarly disagreement acknowledged if present
- [ ] Contemporary context considered appropriately
- [ ] No speculation or personal interpretation presented as fact

## 10. Language and Presentation

- Use respectful Islamic terminology (صلى الله عليه وسلم, رضي الله عنه, etc.)
- Maintain scholarly tone without being inaccessible
- Provide English translations for Arabic terms
- Use proper transliteration (e.g., Qur'an not Koran)
- Structure content for clarity and easy reference
"""

# Primary Fatwa Sources with URLs
PRIMARY_FATWA_SOURCES = {
    'darulifta_deoband': {
        'name': 'Darulifta Deoband',
        'url': 'https://darulifta-deoband.com',
        'description': 'Primary and most authoritative Deobandi fatwa repository',
        'languages': ['Urdu', 'English', 'Arabic'],
        'priority': 1
    },
    'askimam': {
        'name': 'Askimam',
        'url': 'https://askimam.org',
        'description': 'Reliable applied fiqh responses for contemporary issues',
        'languages': ['English'],
        'priority': 2
    },
    'darul_ifta_mahmudiyyah': {
        'name': 'Darul Ifta Mahmudiyyah',
        'url': 'https://daruliftaa.com',
        'description': 'Advanced legal reasoning within Hanafi-Deobandi methodology',
        'languages': ['English', 'Urdu'],
        'priority': 3
    },
    'jamia_banuri': {
        'name': 'Jamia Uloom Islamiyyah (Banuri Town)',
        'url': 'https://banuri.edu.pk',
        'description': 'Major scholarly authority in Pakistan',
        'languages': ['Urdu', 'Arabic'],
        'priority': 4
    },
    'wifaq_uk': {
        'name': 'Wifaq ul Ulama UK',
        'url': 'https://wifaqululama.co.uk',
        'description': 'Contextual fatawa for Muslims in Western environments',
        'languages': ['English'],
        'priority': 5
    },
    'deoband_org': {
        'name': 'Deoband.org',
        'url': 'https://deoband.org',
        'description': 'Expository content on principles, aqida, and methodology',
        'languages': ['English', 'Urdu'],
        'priority': 6
    }
}

# Core Textual Canon
CORE_TEXTS = {
    'aqida': [
        {
            'title': 'Al-Aqida al-Tahawiyyah',
            'author': 'Imam Abu Ja\'far al-Tahawi',
            'category': 'Theology',
            'note': 'Must be interpreted through Hanafi-Maturidi commentaries'
        },
        {
            'title': 'The Absolute Essentials of Islam',
            'author': 'Various Deobandi Scholars',
            'category': 'Theology',
            'note': 'Introductory structured exposition'
        }
    ],
    'fiqh': [
        {
            'title': 'Taleemul Haq',
            'author': 'Various',
            'category': 'Foundational Fiqh',
            'level': 'Beginner'
        },
        {
            'title': 'Behishti Zewar',
            'author': 'Maulana Ashraf Ali Thanwi',
            'category': 'Applied Fiqh',
            'level': 'Intermediate'
        },
        {
            'title': 'Nur al-Idah',
            'author': 'Hasan al-Shurunbulali',
            'category': 'Hanafi Fiqh',
            'level': 'Intermediate'
        },
        {
            'title': 'I\'la al-Sunan',
            'author': 'Zafar Ahmad Usmani',
            'category': 'Advanced Fiqh',
            'level': 'Advanced',
            'note': 'Links fiqh rulings to hadith evidence'
        }
    ],
    'tasawwuf': [
        {
            'title': 'Fazail-e-Amaal',
            'author': 'Muhammad Zakariyya Kandhlawi',
            'category': 'Spiritual Development',
            'note': 'Virtue-based spiritual development'
        }
    ]
}

# Recognized Scholars
RECOGNIZED_SCHOLARS = {
    'foundational': [
        'Muhammad Qasim Nanautawi',
        'Rashid Ahmad Gangohi',
        'Ashraf Ali Thanwi',
        'Mahmud Hasan Deobandi'
    ],
    'contemporary': [
        'Muhammad Taqi Usmani',
        'Ebrahim Desai',
        'Muhammad Zakariyya Kandhlawi'
    ]
}

# Fiqh Terminology
FIQH_TERMINOLOGY = {
    'fard': {'arabic': 'فرض', 'transliteration': 'Fard', 'meaning': 'Obligatory (definitive proof)'},
    'wajib': {'arabic': 'واجب', 'transliteration': 'Wajib', 'meaning': 'Necessary (probabilistic proof)'},
    'sunnah': {'arabic': 'سنت', 'transliteration': 'Sunnah', 'meaning': 'Prophetic practice'},
    'mustahab': {'arabic': 'مستحب', 'transliteration': 'Mustahab', 'meaning': 'Recommended'},
    'mubah': {'arabic': 'مباح', 'transliteration': 'Mubah', 'meaning': 'Permissible'},
    'makruh': {'arabic': 'مکروہ', 'transliteration': 'Makruh', 'meaning': 'Disliked'},
    'haram': {'arabic': 'حرام', 'transliteration': 'Haram', 'meaning': 'Forbidden'}
}

def get_deobandi_guidelines():
    """Return the complete Deobandi guidelines text"""
    return DEOBANDI_GUIDELINES

def get_primary_sources():
    """Return dictionary of primary fatwa sources"""
    return PRIMARY_FATWA_SOURCES

def get_core_texts():
    """Return dictionary of core textual canon"""
    return CORE_TEXTS

def get_recognized_scholars():
    """Return dictionary of recognized scholars"""
    return RECOGNIZED_SCHOLARS

def get_fiqh_terminology():
    """Return dictionary of fiqh terminology"""
    return FIQH_TERMINOLOGY

def format_islamic_response(ruling, evidence, source, classification):
    """
    Format an Islamic response according to Deobandi standards
    
    Args:
        ruling: The Islamic ruling/answer
        evidence: Quranic verse, Hadith, or scholarly consensus
        source: Specific fatwa number, book reference, or scholar name
        classification: فرض/واجب/سنت/مستحب/مباح/مکروہ/حرام
    
    Returns:
        Formatted response string
    """
    return f"""
Ruling: {ruling}

Evidence: {evidence}

Source: {source}

Classification: {classification}

Note: This response is grounded in Hanafi fiqh and Maturidi aqida according to the Darul Uloom Deoband tradition.
"""
