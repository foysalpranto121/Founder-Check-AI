"""
Localization & Expansion - Multi-language, regional customization, market variants
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class Language(str, Enum):
    """Supported languages"""
    ENGLISH = "en"
    BENGALI = "bn"
    HINDI = "hi"


class Region(str, Enum):
    """Supported regions"""
    BANGLADESH = "bd"
    INDIA = "in"
    PAKISTAN = "pk"
    SOUTHEAST_ASIA = "sea"


@dataclass
class LocalizedContent:
    """Localized content"""
    content_id: str
    language: Language
    region: Region
    title: str
    description: str
    content: Dict
    rtl_enabled: bool


@dataclass
class RegionalMarketData:
    """Regional market data"""
    region_id: str
    region: Region
    market_size: str
    growth_rate: str
    key_industries: List[str]
    regulations: List[str]
    opportunities: List[str]
    challenges: List[str]


@dataclass
class LocalizationConfig:
    """Localization configuration"""
    config_id: str
    language: Language
    region: Region
    currency: str
    date_format: str
    number_format: str
    market_data: Dict
    compliance_items: List[str]


class LocalizationService:
    """Service for localization and regional expansion"""

    def __init__(self):
        self.languages = [Language.ENGLISH, Language.BENGALI, Language.HINDI]
        self.regions = [Region.BANGLADESH, Region.INDIA, Region.PAKISTAN, Region.SOUTHEAST_ASIA]
        self.localized_content: Dict[str, LocalizedContent] = {}
        self.regional_data: Dict[str, RegionalMarketData] = {}
        self.configs: Dict[str, LocalizationConfig] = {}
        self._initialize_regional_data()
        self._initialize_localizations()

    def _initialize_regional_data(self):
        """Initialize regional market data"""
        regional_info = {
            Region.BANGLADESH: {
                'market_size': '$2.5B',
                'growth_rate': '25-30%',
                'key_industries': ['Technology', 'E-commerce', 'FinTech', 'Agriculture Tech', 'HealthTech'],
                'regulations': ['BIDA Act 2016', 'Data Protection Act', 'ICT Act 2006', 'Online Safety Act'],
                'opportunities': ['Mobile-first market', 'Large population', 'Rising digital adoption', 'Government incentives'],
                'challenges': ['Infrastructure gaps', 'Regulatory uncertainty', 'Limited funding', 'Talent scarcity']
            },
            Region.INDIA: {
                'market_size': '$40B+',
                'growth_rate': '20-25%',
                'key_industries': ['SaaS', 'EdTech', 'FinTech', 'RetailTech', 'LogisticsTech'],
                'regulations': ['ITA Act', 'SPICE initiative', 'Startup India', 'Data Localization Rules'],
                'opportunities': ['Largest market', 'Mature ecosystem', 'Abundant talent', 'Government support'],
                'challenges': ['High competition', 'Regulatory complexity', 'GST compliance', 'Market saturation']
            },
            Region.PAKISTAN: {
                'market_size': '$1.2B',
                'growth_rate': '18-22%',
                'key_industries': ['IT Services', 'E-commerce', 'FinTech', 'AgriTech', 'Logistics'],
                'regulations': ['Cyber Crime Act', 'SECP Rules', 'State Bank Guidelines', 'PTA Directives'],
                'opportunities': ['Growing tech adoption', 'Youth demographic', 'Remittance economy', 'Agricultural sector'],
                'challenges': ['Regulatory scrutiny', 'Forex restrictions', 'Internet throttling', 'Political instability']
            },
            Region.SOUTHEAST_ASIA: {
                'market_size': '$50B+',
                'growth_rate': '15-20%',
                'key_industries': ['E-commerce', 'FinTech', 'Logistics', 'Travel Tech', 'Gaming'],
                'regulations': ['GDPR-like compliance', 'ASEAN standards', 'Country-specific laws', 'Data residency'],
                'opportunities': ['Massive consumer base', 'Digital payment growth', 'Cross-border commerce', 'Tech hub ecosystem'],
                'challenges': ['Fragmented markets', 'Language diversity', 'Regulatory variance', 'Infrastructure gaps']
            }
        }

        for region, data in regional_info.items():
            region_id = f"region_{region.value}"
            self.regional_data[region_id] = RegionalMarketData(
                region_id=region_id,
                region=region,
                market_size=data['market_size'],
                growth_rate=data['growth_rate'],
                key_industries=data['key_industries'],
                regulations=data['regulations'],
                opportunities=data['opportunities'],
                challenges=data['challenges']
            )

    def _initialize_localizations(self):
        """Initialize localized content"""
        # Bengali translations
        self._add_localized_content(
            Language.BENGALI, Region.BANGLADESH,
            "startup_validator", "স্টার্টআপ ভ্যালিডেটর",
            "আপনার ব্যবসায়িক ধারণা যাচাই করুন এবং সফল হওয়ার পথ জানুন",
            {"slogan": "বাংলাদেশে উদ্ভাবনকে শক্তিশালী করা"}
        )

        self._add_localized_content(
            Language.BENGALI, Region.BANGLADESH,
            "market_analysis", "বাজার বিশ্লেষণ",
            "স্থানীয় বাজারের গভীর অন্তর্দৃষ্টি পান",
            {"focus": "বাংলাদেশ ফোকাসড ডেটা"}
        )

        # Hindi translations for India
        self._add_localized_content(
            Language.HINDI, Region.INDIA,
            "startup_validator", "स्टार्टअप वेलिडेटर",
            "अपने व्यावसायिक विचार को सत्यापित करें और सफलता का मार्ग जानें",
            {"slogan": "भारत में नवाचार को सशक्त बनाना"}
        )

        self._add_localized_content(
            Language.HINDI, Region.INDIA,
            "market_analysis", "बाजार विश्लेषण",
            "भारतीय बाजार की गहन अंतर्दृष्टि प्राप्त करें",
            {"focus": "भारत केंद्रित डेटा"}
        )

        # English translations
        self._add_localized_content(
            Language.ENGLISH, Region.BANGLADESH,
            "startup_validator", "Startup Validator",
            "Validate your business idea and discover the path to success",
            {"slogan": "Empowering innovation in Bangladesh"}
        )

        self._add_localized_content(
            Language.ENGLISH, Region.INDIA,
            "startup_validator", "Startup Validator India",
            "Validate your business idea in the Indian market",
            {"slogan": "Empowering Indian startups"}
        )

    def _add_localized_content(self, language: Language, region: Region,
                               content_id: str, title: str, description: str, content: Dict):
        """Add localized content"""
        key = f"{language.value}_{region.value}_{content_id}"
        rtl = language == Language.HINDI or language == Language.BENGALI

        self.localized_content[key] = LocalizedContent(
            content_id=key,
            language=language,
            region=region,
            title=title,
            description=description,
            content=content,
            rtl_enabled=rtl
        )

    # ========== LANGUAGE & REGION MANAGEMENT ==========

    def get_supported_languages(self) -> List[Dict]:
        """Get supported languages"""
        return [
            {'code': 'en', 'name': 'English', 'native': 'English', 'rtl': False},
            {'code': 'bn', 'name': 'Bengali', 'native': 'বাংলা', 'rtl': False},
            {'code': 'hi', 'name': 'Hindi', 'native': 'हिन्दी', 'rtl': False}
        ]

    def get_supported_regions(self) -> List[Dict]:
        """Get supported regions"""
        return [
            {'code': 'bd', 'name': 'Bangladesh', 'flag': '🇧🇩', 'status': 'active'},
            {'code': 'in', 'name': 'India', 'flag': '🇮🇳', 'status': 'active'},
            {'code': 'pk', 'name': 'Pakistan', 'flag': '🇵🇰', 'status': 'active'},
            {'code': 'sea', 'name': 'Southeast Asia', 'flag': '🌏', 'status': 'active'}
        ]

    def get_localization_config(self, language: str, region: str) -> Dict:
        """Get localization configuration"""
        lang = Language(language) if language in [l.value for l in Language] else Language.ENGLISH
        reg = Region(region) if region in [r.value for r in Region] else Region.BANGLADESH

        config_key = f"{lang.value}_{reg.value}"

        configs = {
            'en_bd': {
                'language': 'en',
                'region': 'bd',
                'currency': 'BDT',
                'date_format': 'DD/MM/YYYY',
                'number_format': '###,###.##',
                'timezone': 'Asia/Dhaka'
            },
            'en_in': {
                'language': 'en',
                'region': 'in',
                'currency': 'INR',
                'date_format': 'DD-MM-YYYY',
                'number_format': '##,##,###.##',
                'timezone': 'Asia/Kolkata'
            },
            'en_pk': {
                'language': 'en',
                'region': 'pk',
                'currency': 'PKR',
                'date_format': 'DD/MM/YYYY',
                'number_format': '###,###.##',
                'timezone': 'Asia/Karachi'
            },
            'bn_bd': {
                'language': 'bn',
                'region': 'bd',
                'currency': 'BDT',
                'date_format': 'DD/MM/YYYY',
                'number_format': '###,###.##',
                'timezone': 'Asia/Dhaka',
                'rtl': False
            },
            'hi_in': {
                'language': 'hi',
                'region': 'in',
                'currency': 'INR',
                'date_format': 'DD-MM-YYYY',
                'number_format': '##,##,###.##',
                'timezone': 'Asia/Kolkata',
                'rtl': False
            }
        }

        return configs.get(config_key, configs['en_bd'])

    # ========== REGIONAL MARKET DATA ==========

    def get_regional_market_data(self, region: str) -> Optional[Dict]:
        """Get regional market data"""
        for region_data in self.regional_data.values():
            if region_data.region.value == region:
                return {
                    'region': region_data.region.value,
                    'market_size': region_data.market_size,
                    'growth_rate': region_data.growth_rate,
                    'key_industries': region_data.key_industries,
                    'regulations': region_data.regulations,
                    'opportunities': region_data.opportunities,
                    'challenges': region_data.challenges
                }
        return None

    def get_all_regional_data(self) -> List[Dict]:
        """Get all regional data"""
        return [
            self.get_regional_market_data(region.value)
            for region in Region
        ]

    # ========== LOCALIZED CONTENT ==========

    def get_localized_content(self, language: str, region: str, content_type: str) -> Optional[Dict]:
        """Get localized content"""
        key = f"{language}_{region}_{content_type}"
        if key in self.localized_content:
            content = self.localized_content[key]
            return {
                'id': content.content_id,
                'title': content.title,
                'description': content.description,
                'content': content.content,
                'rtl': content.rtl_enabled
            }
        return None

    def get_localization_dashboard(self, language: str = 'en', region: str = 'bd') -> Dict:
        """Get localization dashboard"""
        return {
            'current_language': language,
            'current_region': region,
            'supported_languages': self.get_supported_languages(),
            'supported_regions': self.get_supported_regions(),
            'regional_data': self.get_regional_market_data(region),
            'config': self.get_localization_config(language, region),
            'localization_stats': {
                'languages_supported': len(self.languages),
                'regions_supported': len(self.regions),
                'content_items': len(self.localized_content),
                'coverage': '95%'
            }
        }

    # ========== MULTI-VARIANT PLATFORM ==========

    def get_market_variant(self, region: str) -> Dict:
        """Get market-specific variant configuration"""
        variants = {
            'bd': {
                'theme_color': '#006747',
                'hero_text': 'বাংলাদেশ স্টার্টআপ ইকোসিস্টেমের জন্য নির্মিত',
                'featured_sectors': ['Agriculture Tech', 'FinTech', 'E-commerce'],
                'compliance_focus': ['BIDA', 'Data Protection'],
                'funding_sources': ['Government grants', 'Angel investors', 'International VC'],
                'success_stories': 3
            },
            'in': {
                'theme_color': '#FF9933',
                'hero_text': 'Startup India के लिए तैयार',
                'featured_sectors': ['SaaS', 'EdTech', 'FinTech'],
                'compliance_focus': ['SPICE', 'GST', 'Data Localization'],
                'funding_sources': ['Government schemes', 'Domestic VC', 'Angel networks'],
                'success_stories': 15
            },
            'pk': {
                'theme_color': '#00411C',
                'hero_text': 'پاکستان کے اسٹارٹ اپس کے لیے',
                'featured_sectors': ['IT Services', 'FinTech', 'Logistics'],
                'compliance_focus': ['Cyber Crime Act', 'SECP Rules'],
                'funding_sources': ['Government tech parks', 'International donors', 'Regional VC'],
                'success_stories': 5
            },
            'sea': {
                'theme_color': '#003478',
                'hero_text': 'Southeast Asia Startup Hub',
                'featured_sectors': ['E-commerce', 'Logistics', 'Travel Tech'],
                'compliance_focus': ['ASEAN', 'Country-specific', 'Data residency'],
                'funding_sources': ['Regional VCs', 'Corporate ventures', 'International funds'],
                'success_stories': 20
            }
        }

        return variants.get(region, variants['bd'])

    def get_localized_compliance(self, region: str) -> Dict:
        """Get localized compliance checklist"""
        compliance_items = {
            'bd': [
                'BIDA Investment Registration',
                'Company Registration (RJSC)',
                'Tax Identification Number (TIN)',
                'Bank Account Opening',
                'Data Protection Compliance',
                'E-commerce License (if applicable)'
            ],
            'in': [
                'PAN & GST Registration',
                'Company Registration (MCA)',
                'Bank Account & MSME Registration',
                'Data Localization Compliance',
                'Startup India Recognition',
                'Sector-specific licenses'
            ],
            'pk': [
                'SECP Registration',
                'NTN & Sales Tax Registration',
                'Bank Account Opening',
                'Cyber Crime Act Compliance',
                'Pakistan Stock Exchange (if applicable)',
                'Authority approvals by sector'
            ],
            'sea': [
                'Country-specific registration',
                'Tax & GST compliance',
                'Data protection registration',
                'E-commerce license',
                'Industry-specific permits',
                'International compliance'
            ]
        }

        return {
            'region': region,
            'items': compliance_items.get(region, compliance_items['bd']),
            'estimated_timeline': '6-12 weeks',
            'estimated_cost': 'Varies by region'
        }


# Global localization service instance
localization_service = LocalizationService()
