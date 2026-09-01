name = input("Enter your name: ")

education = input("Enter your education: ")

experience = input("Enter your experience level: ")

skills_input = input(
    "Enter your skills separated by commas: "
)

target_role = input(
    "Enter your target role: "
)


skills = [
    skill.strip()
    for skill in skills_input.split(",")
]


user_profile = {
    "name": name,
    "education": education,
    "experience": experience,
    "skills": skills,
    "target_role": target_role
}


print("\nYour Career Profile")
print("-------------------")

print("Name:", user_profile["name"])
print("Education:", user_profile["education"])
print("Experience:", user_profile["experience"])

print("\nSkills:")

for skill in user_profile["skills"]:
    print("-", skill)

print("\nTarget Role:", user_profile["target_role"])