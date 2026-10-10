"""Starter content. Seeded once on first `migrate`; afterwards everything is edited in the admin panel."""

PAGES = {
    "home": dict(
        seo_title="Study Abroad & Education Counselling",
        meta_description="Study abroad counselling, university application support and visa documentation guidance from Bhumi Pathways Consultancy.",
        eyebrow="Study abroad counselling",
        hero_title="Chart the route to the right university abroad.",
        hero_text="Honest, personal guidance on courses, applications and visa paperwork, from first question to pre-departure.",
    ),
    "about": dict(
        seo_title="About Us",
        meta_description="Learn how Bhumi Pathways Consultancy supports students with study abroad counselling, applications and visa documentation.",
        hero_title="About Bhumi Pathways",
        hero_text="'Bhumi' means land. We help students find the right ground to build their education on.",
        section_title="Our principles",
        body=("<h2>What we do</h2>"
              "<p>Bhumi Pathways Consultancy is an education and study abroad consultancy. We work with students and families to choose suitable courses and destinations, prepare applications and organise visa documentation.</p>"
              "<p><em>Placeholder: add your founding story, team members, office locations, registrations and partner institutions here once confirmed. Only publish credentials you can document.</em></p>"),
    ),
    "services": dict(
        seo_title="Services",
        meta_description="Course shortlisting, application support, SOP guidance, funding guidance and visa documentation support for students going abroad.",
        hero_title="Services for every stage",
        hero_text="Choose the support you need, from a single review to end-to-end guidance.",
        section_title="How an engagement works",
        body="<p>Service fees are confirmed in writing before you commit. <em>Placeholder: add your fee structure here when finalised.</em></p>",
    ),
    "destinations": dict(
        seo_title="Study Destinations",
        meta_description="Explore study abroad destinations: USA, UK, Canada, Australia, Germany and Ireland. Typical intakes and what to consider.",
        hero_title="Study destinations",
        hero_text="Typical intakes and considerations for each country. Always confirm details with the institution.",
        notice="Information is general and may change. Entry requirements, fees, intakes and immigration rules vary by institution and are set by the relevant authorities.",
    ),
    "visa": dict(
        seo_title="Visa Assistance",
        meta_description="Student visa documentation support: checklists, form guidance and interview preparation. No visa outcome is guaranteed.",
        hero_title="Visa assistance",
        hero_text="Organised paperwork and clear guidance, so your application is complete and accurate.",
        section_title="Documents commonly requested",
        section_intro="This is a general list. Your destination's official immigration website is the final authority.",
        body=("<h2>What we help with</h2><ul>"
              "<li>Country-specific document checklists</li>"
              "<li>Reviewing forms and supporting documents for completeness and consistency</li>"
              "<li>Guidance on financial documentation</li>"
              "<li>Interview preparation tips</li></ul>"),
        notice="Visa decisions are made solely by government immigration authorities. Bhumi Pathways Consultancy does not guarantee any visa outcome and does not influence decisions. Submit only genuine, truthful documents.",
    ),
    "faqs": dict(
        seo_title="FAQs",
        meta_description="Answers to common questions about studying abroad, applications, visas and working with Bhumi Pathways Consultancy.",
        hero_title="Frequently asked questions",
    ),
    "contact": dict(
        seo_title="Contact",
        meta_description="Book a study abroad consultation or ask a question. Contact Bhumi Pathways Consultancy by form, phone, email or WhatsApp.",
        hero_title="Contact us",
        hero_text="Send an enquiry or message us directly.",
        body="<p class=\"small text-muted\">Placeholder: add a map link or directions once your office address is confirmed.</p>",
    ),
    "privacy": dict(
        seo_title="Privacy Policy",
        meta_description="How Bhumi Pathways Consultancy collects and uses personal information.",
        hero_title="Privacy Policy",
        notice="Template text. Have it reviewed by a qualified legal professional and add your registered business name, address and grievance contact before launch.",
        body=("<h2>Information we collect</h2><p>When you submit an enquiry we collect your name, email address, phone number, preferred country, study level and any message you write. We also record the date and time of your enquiry and your consent.</p>"
              "<h2>How we use it</h2><p>We use this information to respond to your enquiry, provide the services you request and keep a record of our communications. We send an acknowledgement email and may contact you by phone, email or WhatsApp.</p>"
              "<h2>Sharing</h2><p>We do not sell your personal information. We may share it with service providers that help us operate (for example hosting and email) and, with your agreement, with institutions you apply to. We may disclose it where required by law.</p>"
              "<h2>Retention and security</h2><p>We keep enquiries only as long as needed for the purposes above. Access to enquiry records is limited to authorised staff through authenticated accounts.</p>"
              "<h2>Your choices</h2><p>You may ask us to access, correct or delete your information, or withdraw your consent to be contacted, by writing to us at the email address shown on the Contact page.</p>"
              "<h2>Cookies</h2><p>This website uses only essential cookies (for security and form submission). If analytics are added, this policy will be updated.</p>"),
    ),
    "terms": dict(
        seo_title="Terms of Use",
        meta_description="Terms of use for the Bhumi Pathways Consultancy website.",
        hero_title="Terms of Use",
        notice="Template text. Have it reviewed by a qualified legal professional before launch.",
        body=("<h2>Information only</h2><p>Content on this website is general information and is not legal, immigration or financial advice. Requirements and fees change; confirm with the institution or authority.</p>"
              "<h2>No guarantees</h2><p>We do not guarantee admission, scholarships, visas or any other outcome. Decisions are made by institutions and government authorities.</p>"
              "<h2>Your responsibilities</h2><p>You must provide accurate and genuine information and documents. Submitting false information may lead to refusal and other consequences.</p>"
              "<h2>Fees</h2><p>Service fees, if any, are communicated and agreed in writing before services begin.</p>"
              "<h2>Third-party links</h2><p>We are not responsible for the content of external websites.</p>"
              "<h2>Changes</h2><p>We may update these terms. Continued use of the website means you accept the updated terms.</p>"),
    ),
}

MENU = [
    ("header", "Home", "/"), ("header", "About Us", "/about/"), ("header", "Services", "/services/"),
    ("header", "Study Destinations", "/destinations/"), ("header", "Visa Assistance", "/visa-assistance/"),
    ("header", "FAQs", "/faqs/"), ("header", "Contact", "/contact/"),
    ("footer", "About Us", "/about/"), ("footer", "Services", "/services/"),
    ("footer", "Study Destinations", "/destinations/"), ("footer", "Visa Assistance", "/visa-assistance/"),
    ("footer", "FAQs", "/faqs/"), ("footer", "Contact", "/contact/"),
    ("legal", "Privacy Policy", "/privacy-policy/"), ("legal", "Terms", "/terms/"),
]

# Intakes are typical patterns only; always confirm with each institution.
DESTINATIONS = [
    dict(name="United States", flag="🇺🇸", intakes="Fall (Aug–Sep), Spring (Jan)",
         intro="A very large and varied higher-education system, with strong emphasis on flexible degree structures and research.",
         points="Wide choice of majors and the option to explore before specialising\nResearch and project-based learning at many universities\nStandardised tests may be requested by some programmes"),
    dict(name="United Kingdom", flag="🇬🇧", intakes="September, January (select courses)",
         intro="Focused, subject-specific degrees. Many undergraduate courses run for three years and many master's courses for one.",
         points="Shorter, specialised degree structures\nCentralised undergraduate applications through UCAS\nCourse-specific entry requirements"),
    dict(name="Canada", flag="🇨🇦", intakes="September, January, May (varies)",
         intro="Universities and colleges offering degree, diploma and applied programmes, many with co-op or practical components.",
         points="Mix of universities and applied-learning colleges\nCo-op options on selected programmes\nProvincial rules can affect eligibility and processes"),
    dict(name="Australia", flag="🇦🇺", intakes="February, July (some courses have more)",
         intro="A structured system with clear course pathways, including foundation and diploma routes into degrees.",
         points="Pathway programmes available at some institutions\nDefined study-level frameworks\nVisa requirements include financial and health checks"),
    dict(name="Germany", flag="🇩🇪", intakes="Winter (Oct), Summer (Apr)",
         intro="Known for engineering and applied sciences, with many public universities and a growing number of English-taught programmes.",
         points="English-taught and German-taught options\nProgramme-specific language requirements\nBlocked-account style financial proof is commonly part of visa steps"),
    dict(name="Ireland", flag="🇮🇪", intakes="September, January (select courses)",
         intro="English-speaking country with universities and technological universities, popular for business, computing and life sciences.",
         points="English-medium teaching\nRange of taught postgraduate courses\nAccommodation planning matters early in major cities"),
]

SERVICES = [
    ("Profile review & course shortlisting", "We look at your academics, interests and budget, then help you build a realistic shortlist of courses and institutions."),
    ("Application support", "Guidance on documents, deadlines and forms so that each application is complete, accurate and submitted on time."),
    ("SOP, LOR & CV guidance", "Feedback on your statement of purpose, recommendation letters and CV. The writing remains your own."),
    ("Funding & scholarship guidance", "Help understanding tuition, living costs, education loans and scholarships you may be eligible to apply for."),
    ("Visa documentation support", "Checklists, form guidance and interview preparation tips. Visa decisions are made solely by the immigration authority."),
    ("Pre-departure briefing", "Practical guidance on accommodation, travel, insurance and settling in before you leave."),
]

STEPS = [
    ("Talk to a counsellor", "Share your goals and background in a consultation."),
    ("Shortlist options", "Compare courses, countries, costs and entry requirements."),
    ("Apply", "Prepare documents and submit applications."),
    ("Prepare your visa file", "Organise financial and academic documents."),
    ("Get ready to travel", "Pre-departure guidance before you fly."),
]

PRINCIPLES = [
    ("Honest advice", "We tell you what a course or country can and cannot offer, including costs and risks."),
    ("No guarantees", "Admission and visa decisions belong to institutions and governments. We never promise outcomes."),
    ("Your decision", "We lay out options and trade-offs. You and your family choose."),
    ("Clear communication", "Plain answers, written checklists and timely follow-ups."),
]

VISA_DOCS = [
    "Valid passport", "Offer / admission letter from the institution", "Academic transcripts and certificates",
    "English-language test score, if required", "Proof of funds and financial documents",
    "Statement of purpose, if required", "Passport-size photographs",
    "Medical and police clearance, where the country requires them",
]

FAQS = [
    ("Do you guarantee admission or a visa?", "No. Admission decisions are made by institutions and visa decisions by government authorities. We guide you on requirements and help you prepare a complete, accurate application."),
    ("Which countries can you advise on?", "Our current focus is the United States, United Kingdom, Canada, Australia, Germany and Ireland. Contact us if you are considering another destination."),
    ("When should I start the process?", "Ideally 9–12 months before your intended intake, as tests, documents, applications and visa steps all take time."),
    ("Do I need an English-language test?", "It depends on the country, institution and course. Some accept alternatives. A counsellor can check the requirement for your shortlisted programmes."),
    ("What does a consultation cost?", "Fees are shared by our team when you enquire. Please ask about charges before you sign up to any service."),
    ("How is my personal data used?", "We use the details you submit only to respond to your enquiry and provide the services you request. See our Privacy Policy for details."),
    ("Can I get help with an education loan or scholarships?", "We can explain the options and what documents lenders and scholarship providers usually ask for. Approval is decided by the lender or provider."),
]
