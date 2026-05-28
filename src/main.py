from textnode import Inline, TextNode, Block
from htmlnode import HTMLNode, LeafNode, ParentNode
import re
import os
import shutil

def main():

    copy_files_to_public("static", "public")
    generate_pages_recursive("content", "template.html", "public")

def text_node_to_html_node(text_node):
    if text_node.text_type == Inline.TEXT:
        return LeafNode(None,text_node.text)
    elif text_node.text_type == Inline.BOLD:
        return LeafNode("b",text_node.text)
    elif text_node.text_type == Inline.ITALIC:
        return LeafNode("i",text_node.text)
    elif text_node.text_type == Inline.CODE:
        return LeafNode("code",text_node.text)
    elif text_node.text_type == Inline.LINK:
        return LeafNode("a",text_node.text, {"href": text_node.url})
    elif text_node.text_type == Inline.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception("not supported tag")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return_list = []
    for node in old_nodes:
        if node.text_type != Inline.TEXT:
            return_list.append(node)
        else:
            text = node.text.split(delimiter)
            if len(text) % 2 != 0:
                for i in range(0, len(text)):
                    if text[i] != "" and i % 2 == 0:
                        return_list.append(TextNode(text[i], Inline.TEXT))
                    elif text[i] != "":
                        return_list.append(TextNode(text[i], text_type))
            else:
                raise Exception("unmatched delimiter")
    return return_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    return_list = []
    for node in old_nodes:
        if node.text_type == Inline.TEXT:
            image = extract_markdown_images(node.text)
            if len(image) == 0:
                return_list.append(node)
                continue
            text = node.text

            for i in image:
                image_alt = i[0]
                image_link = i[1]
                text = text.split(f"![{image_alt}]({image_link})", 1)
                if text[0] != "":
                    return_list.append(TextNode(text[0], Inline.TEXT))
                return_list.append(TextNode(image_alt, Inline.IMAGE, image_link))
                text = text[1]
            if text != "":
                return_list.append(TextNode(text, Inline.TEXT))
        else:
            return_list.append(node)    
    return return_list

def split_nodes_link(old_nodes):
    return_list = []
    for node in old_nodes:
        if node.text_type == Inline.TEXT:
            link = extract_markdown_links(node.text)
            if len(link) == 0:
                return_list.append(node)
                continue
            text = node.text

            for i in link:
                link_alt = i[0]
                link_link = i[1]
                text = text.split(f"[{link_alt}]({link_link})", 1)
                if text[0] != "":
                    return_list.append(TextNode(text[0], Inline.TEXT))
                return_list.append(TextNode(link_alt, Inline.LINK, link_link))
                text = text[1]
            if text != "":
                return_list.append(TextNode(text, Inline.TEXT))
        else:
            return_list.append(node)   
    return return_list

def text_to_textnodes(text):
    return_list = []
    node = [TextNode(text, Inline.TEXT)]
    return_list.extend(split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(node, "**", Inline.BOLD), "_", Inline.ITALIC), "`", Inline.CODE))))
    return return_list

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return_list = []
    for block in blocks:

        cleaned_block = block.strip()

        if cleaned_block != "":
            return_list.append(cleaned_block)
    return return_list

def block_to_block_type(single_block):
    if single_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return Block.HEADING
    if single_block[0:3] == "```" and single_block[-3:] == "```":
        if len(single_block.split("\n")) >= 2:
            return Block.CODE
    if single_block.startswith(">"):
        lines = single_block.split("\n")
        is_it = True
        for i in lines:
            if not i.startswith(">"):
                is_it = False
                break
        if is_it:
            return Block.QUOTE
    if single_block.startswith("- "):
        lines = single_block.split("\n")
        is_it = True
        for i in lines:
            if not i.startswith("- "):
                is_it = False
                break
        if is_it:
            return Block.UNORDERED_LIST
    if single_block[0:3] == "1. ":
        lines = single_block.split("\n")
        is_it = True

        for i in range(0, len(lines)):
            if not lines[i].startswith( (f"{i+1}. ")):
                is_it = False
                break

        if is_it:
            return Block.ORDERED_LIST
    return Block.PARAGRAPH

def block_type_to_tag(blocktype, block):
    if blocktype == Block.QUOTE:
        return "blockquote"
    if blocktype == Block.UNORDERED_LIST:
        return "ul"
    if blocktype == Block.ORDERED_LIST:
        return "ol"
    if blocktype == Block.CODE:
        return "pre" 
    if blocktype == Block.PARAGRAPH:
        return "p"
    if blocktype == Block.HEADING:
        if block.startswith("# "):
            return "h1"
        if block.startswith("## "):
            return "h2"
        if block.startswith("### "):
            return "h3"
        if block.startswith("#### "):
            return "h4"
        if block.startswith("##### "):
            return "h5"
        if block.startswith("###### "):
            return "h6"
        raise Exception("not matching header")
    raise Exception("unknown block type ")
def text_to_children(text):
    lower_children = []
    text_nodes = text_to_textnodes(text)
    for j in text_nodes:
        lower_children.append(text_node_to_html_node(j))
    return lower_children



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        blocktag = block_type_to_tag(blocktype, block)
        top_html_block = ParentNode(blocktag, [], None)
        if blocktype == Block.ORDERED_LIST:
            lines = block.split("\n")
            middle_children = []
            for i in range(0, len(lines)):
                marker = f"{i + 1}. "
                lines[i] = lines[i][len(marker):]
                lines[i] = lines[i].strip()
                middle_html_block = ParentNode("li", text_to_children(lines[i]), None)
                middle_children.append(middle_html_block) 
            top_html_block.children = middle_children

        if blocktype == Block.PARAGRAPH:
            paragraph_text = block.replace("\n", " ")
            paragraph_text = paragraph_text.strip()
            top_html_block.children = text_to_children(paragraph_text)

        if blocktype == Block.QUOTE:
            lines = block.split("\n")
            for i in range(0, len(lines)):
                marker = ">"
                lines[i] = lines[i][len(marker):].strip()

            lines = " ".join(lines)
            top_html_block.children = text_to_children(lines)
        
        if blocktype == Block.UNORDERED_LIST:
            lines = block.split("\n")
            middle_children = []
            for i in range(0, len(lines)):
                marker = "- "
                lines[i] = lines[i].strip()
                lines[i] = lines[i][len(marker):]
                middle_html_block = ParentNode("li", text_to_children(lines[i]), None)
                middle_children.append(middle_html_block) 
            top_html_block.children = middle_children

        if blocktype == Block.CODE:
            code_text = block.strip("```").removeprefix("\n")
            text_node = TextNode(code_text, Inline.TEXT)
            middle_html_block = ParentNode("code", [text_node_to_html_node(text_node)], None)
            top_html_block.children = [middle_html_block]
        if blocktype == Block.HEADING:
            if blocktype == Block.HEADING:
                marker = 0
                if block.startswith("# "):
                    marker = 2
                if block.startswith("## "):
                    marker = 3
                if block.startswith("### "):
                    marker = 4
                if block.startswith("#### "):
                    marker = 5
                if block.startswith("##### "):
                    marker = 6
                if block.startswith("###### "):
                    marker = 7
                header_text = block[marker:]
                top_html_block.children = text_to_children(header_text)
        html_nodes.append(top_html_block)
    return ParentNode("div", html_nodes, None)

def copy_files_to_public(src, dst):

    if os.path.exists(dst):
        shutil.rmtree(dst)
    if os.path.exists(src):
        inside = os.listdir(src)
        os.mkdir(dst)
        if inside:
            for i in inside:
                if os.path.isfile(os.path.join(src, i)):
                    shutil.copy(os.path.join(src, i), dst )
                elif os.path.isdir(os.path.join(src, i)):
                    copy_files_to_public(os.path.join(src, i), os.path.join(dst, i))
    else:
        raise Exception("source directorydoes not exist")
    
def extract_title(markdown):
    if markdown.startswith("# "):
        title = markdown.split("\n", 1)[0]
        title = title.strip("# ")
        return title
    else:
        raise Exception("Title not found")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
            markdown = f.read()
            f.close()
    with open(template_path) as f:
            template = f.read()
            f.close()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    dir_name = os.path.dirname(dest_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def folder_crawler(dir):
    file_path_list = []
    for i in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, i)):
            file_path_list.append(os.path.join(dir, i))
        elif os.path.isdir(os.path.join(dir, i)):
            file_path_list.extend(folder_crawler(os.path.join(dir, i)))
    return file_path_list

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = folder_crawler(dir_path_content)
    for i in files:

        relativ_path = os.path.relpath(i, dir_path_content)
        htlm_relativ_path = os.path.splitext(relativ_path)[0] + ".html"
        dest_path = os.path.join(dest_dir_path, htlm_relativ_path)

        generate_page(i, template_path, dest_path)
    
    

main()