universities = [
    {
        "name": "Bethesda University",
        "domain": "bethesdauniversity.edu",
        "potential_paths": [
            "/student-life/clubs",
            "/campus-life/organizations", 
            "/clubs",
            "/student-activities",
            "/student-organizations"
        ]
    },
    {
        "name": "Bethune-Cookman University",
        "domain": "cookman.edu",
        "potential_paths": [
            "/student-life/clubs",
            "/campus-life/organizations",
            "/clubs", 
            "/student-activities",
            "/student-organizations"
        ]
    },
    {
        "name": "Beulah Heights University",
        "domain": "beulah.edu",
        "potential_paths": [
            "/student-life/clubs",
            "/campus-life/organizations",
            "/clubs",
            "/student-activities", 
            "/student-organizations"
        ]
    },
    {
        "name": "Bevill State Community College",
        "domain": "bscc.edu",
        "potential_paths": [
            "/student-life/clubs",
            "/campus-life/organizations",
            "/clubs",
            "/student-activities",
            "/student-organizations"
        ]
    },
    {
        "name": "Big Bend Community College",
        "domain": "bigbend.edu",
        "potential_paths": [
            "/student-life/clubs",
            "/campus-life/organizations", 
            "/clubs",
            "/student-activities",
            "/student-organizations"
        ]
    },
    {
        "name": "Biola University",
        "domain": "biola.edu",
        "potential_paths": [
            "/student-life/clubs",
            "/campus-life/organizations",
            "/clubs",
            "/student-activities",
            "/student-organizations"
        ]
    },
    {
        "name": "Bishop State Community College",
        "domain": "bishop.edu",
        "potential_paths": [
            "/student-life/clubs",
            "/campus-life/organizations",
            "/clubs", 
            "/student-activities",
            "/student-organizations"
        ]
    },
    {
        "name": "Black Hills State University",
        "domain": "bhsu.edu",
        "potential_paths": [
            "/student-life/clubs",
            "/campus-life/organizations",
            "/clubs",
            "/student-activities",
            "/student-organizations"
        ]
    },
    {
        "name": "Blackfeet Community College",
        "domain": "bfcc.edu",
        "potential_paths": [
            "/student-life/clubs",
            "/campus-life/organizations",
            "/clubs",
            "/student-activities",
            "/student-organizations"
        ]
    },
    {
        "name": "Bladen Community College",
        "domain": "bladencc.edu",
        "potential_paths": [
            "/student-life/clubs",
            "/campus-life/organizations",
            "/clubs",
            "/student-activities", 
            "/student-organizations"
        ]
    },
    {
        "name": "Blue Mountain Community College",
        "domain": "bluecc.edu",
        "potential_paths": [
            "/student-life/clubs",
            "/campus-life/organizations",
            "/clubs",
            "/student-activities",
            "/student-organizations"
        ]
    }
]

# Data fields to extract
ORGANIZATION_FIELDS = [
    "Category",
    "Organization Name", 
    "Organization Link",
    "Logo Link",
    "Description",
    "Email",
    "Phone Number",
    "LinkedIn Link",
    "Instagram Link", 
    "Facebook Link",
    "Twitter Link",
    "YouTube Link",
    "TikTok Link"
]

# Common selectors for different website platforms
PLATFORM_SELECTORS = {
    "engage": {
        "organization_list": ".organizations-list .organization-item",
        "organization_name": ".organization-name, .org-name, h3, h4",
        "organization_link": "a[href*='/organization/'], a[href*='/club/']",
        "category": ".category, .org-category, .tag",
        "description": ".description, .org-description, p",
        "logo": ".logo img, .organization-logo img, .org-image img"
    },
    "campus_labs": {
        "organization_list": ".organization-card, .org-card",
        "organization_name": ".org-name, .organization-title, h3",
        "organization_link": "a[href*='/organization/'], a[href*='/org/']",
        "category": ".category, .org-type",
        "description": ".description, .org-description",
        "logo": ".org-logo img, .logo img"
    },
    "presence": {
        "organization_list": ".org-item, .organization",
        "organization_name": ".org-name, h3, h4",
        "organization_link": "a[href*='/org/'], a[href*='/organization/']",
        "category": ".category, .type",
        "description": ".description, .about",
        "logo": ".org-logo img, img[alt*='logo']"
    },
    "generic": {
        "organization_list": ".organization, .club, .org, .student-org",
        "organization_name": "h1, h2, h3, h4, .name, .title",
        "organization_link": "a",
        "category": ".category, .type, .tag",
        "description": ".description, .about, p",
        "logo": "img"
    }
}

# Social media patterns for link extraction
SOCIAL_MEDIA_PATTERNS = {
    "LinkedIn": [
        "linkedin.com",
        "linkedin"
    ],
    "Instagram": [
        "instagram.com",
        "instagram"
    ],
    "Facebook": [
        "facebook.com",
        "facebook"
    ],
    "Twitter": [
        "twitter.com",
        "x.com",
        "twitter"
    ],
    "YouTube": [
        "youtube.com",
        "youtu.be",
        "youtube"
    ],
    "TikTok": [
        "tiktok.com",
        "tiktok"
    ]
}