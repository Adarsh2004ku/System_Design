import re
import os

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\- ]', '', text)
    text = text.replace(' ', '-')
    return text

def main():
    with open('readme.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the global Table of Contents
    toc_match = re.search(r'# Table of contents\n\n(.*?)(?=\n# |\Z)', content, re.DOTALL)
    if not toc_match:
        print("TOC not found")
        return
    
    toc_content = toc_match.group(1)
    
    # Write the content.md
    with open('content.md', 'w', encoding='utf-8') as f:
        f.write("# Content Page\n\n")
        f.write(toc_content)
        
    print("Created content.md")

    # Parse the TOC to get chapters and their sub-topics
    lines = toc_content.split('\n')
    chapters = []
    current_chapter = None
    
    for line in lines:
        if line.startswith('- **'):
            chapter_name = line.replace('- **', '').replace('**', '').strip()
            current_chapter = {
                'name': chapter_name,
                'topics': [],
                'toc_lines': []
            }
            chapters.append(current_chapter)
        elif line.strip().startswith('- [') and current_chapter is not None:
            match = re.search(r'\[(.*?)\]\(\#(.*?)\)', line)
            if match:
                topic_title = match.group(1)
                topic_slug = match.group(2)
                current_chapter['topics'].append({
                    'title': topic_title,
                    'slug': topic_slug
                })
                current_chapter['toc_lines'].append(line.strip())

    # Extract topics content
    # Find all topics starting with '# '
    topic_contents = {}
    
    # Split content by top level heading
    parts = re.split(r'\n# ', '\n' + content)
    for part in parts:
        if not part.strip():
            continue
        lines = part.split('\n', 1)
        title = lines[0].strip()
        body = lines[1] if len(lines) > 1 else ''
        topic_contents[slugify(title)] = '# ' + title + '\n' + body

    # Write each chapter
    for idx, chapter in enumerate(chapters):
        file_name = slugify(chapter['name']) + '.md'
        
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"# {chapter['name']}\n\n")
            f.write("## Content Page and Index\n\n")
            
            for line in chapter['toc_lines']:
                f.write(f"{line}\n")
            
            f.write("\n---\n\n")
            
            for topic in chapter['topics']:
                slug = topic['slug']
                if slug in topic_contents:
                    f.write(topic_contents[slug])
                    f.write("\n\n")
                else:
                    print(f"Warning: Content for topic '{topic['title']}' (slug: {slug}) not found.")
                    
        print(f"Created {file_name}")

if __name__ == '__main__':
    main()
