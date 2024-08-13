# with open("D:\\Downloads\\blogs.txt", 'r', encoding='utf-8') as file:
#     content = file.read()

# # Replace multiple consecutive blank lines with an empty string
# # This pattern matches two or more blank lines (\n\n+)
# content = content.replace('\n\n\n', '')

# # Save the modified content back to the file
# with open('D:\\Downloads\\blogs1.txt', 'w', encoding='utf-8') as file:
#     file.write(content)

import re

# Load the text file with UTF-8 encoding
with open('D:\\Downloads\\blogs.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Replace multiple consecutive blank lines with an empty string
content = re.sub(r'\n\s*\n', '\n\n', content)

# Save the modified content back to the file
with open('D:\\Downloads\\blogs2.txt', 'w', encoding='utf-8') as file:
    file.write(content)
print("Done...")
