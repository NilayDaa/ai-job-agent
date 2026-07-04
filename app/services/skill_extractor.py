import re


KNOWN_SKILLS = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#",
    "Go", "Rust", "PHP", "Ruby", "Kotlin", "Swift",

    # Backend
    "FastAPI", "Django", "Flask", "Spring Boot",
    "ASP.NET", "Node.js", "Express",

    # Frontend
    "React", "Angular", "Vue", "HTML", "CSS",
    "Bootstrap", "Tailwind CSS",

    # Databases
    "SQL", "SQLite", "PostgreSQL", "MySQL",
    "MongoDB", "Redis",

    # DevOps & Cloud
    "Docker", "Kubernetes", "Git", "GitHub",
    "Linux", "Azure", "AWS", "Google Cloud",
    "Terraform", "Jenkins",

    # AI / Data
    "Machine Learning", "Deep Learning",
    "TensorFlow", "PyTorch", "LangChain",
    "OpenAI", "Gemini", "FAISS",
    "Pandas", "NumPy",

    # Testing
    "Playwright",

    # Cleaning Skills
    "Cleaning",
    "Commercial Cleaning",
    "Office Cleaning",
    "Hotel Cleaning",
    "Housekeeping",
    "Apartment Cleaning",
    "Deep Cleaning",
    "Floor Cleaning",
    "Floor Care",
    "Window Cleaning",
    "Sanitation",
    "Disinfection",
    "Waste Management",
    "Laundry",
    "Dusting",
    "Vacuuming",
    "Mopping",
    "Restroom Cleaning",
    "Kitchen Cleaning",

    # Cleaning Equipment
    "Floor Scrubber",
    "Vacuum Cleaner",
    "Pressure Washer",
    "Steam Cleaner",
    "Cleaning Chemicals",

    # Soft Skills
    "Customer Service",
    "Communication",
    "Teamwork",
    "Time Management",
    "Problem Solving",
    "Attention to Detail",
    "Reliability",
    "Adaptability",
    "Leadership",

    # Languages
    "English",
    "Finnish",
    "Swedish",
]

def extract_skills(text: str):

    found_skills = []

    text = text.lower()

    for skill in KNOWN_SKILLS:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(found_skills)