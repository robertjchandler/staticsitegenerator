from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if node.text.count(delimiter) != 2:
                raise Exception("invalid Markdown syntax")
            
            split_node = node.text.split(delimiter)
            new_nodes.append(TextNode(split_node[0], TextType.TEXT))
            new_nodes.append(TextNode(split_node[1], text_type))
            new_nodes.append(TextNode(split_node[2], TextType.TEXT))
    return new_nodes
