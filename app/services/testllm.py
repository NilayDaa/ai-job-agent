from app.services.llm_service import llm

response = llm.generate(
    "Explain in two sentences why Python is popular."
)

print(response)