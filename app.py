from word_to_root import WordToRoot
import os
from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher


def save_to_neo4j(graph, word, root):
    print(f'正在处理：{root} -> {word}')

    tx = graph.begin()
    nodes = NodeMatcher(graph)

    tree = nodes.match("Word", name=root).first()
    if not tree:
        tree = Node("Word", name=root)
        tx.create(tree)

    leaf = nodes.match("Word", name=word).first()
    if not leaf:
        leaf = Node("Word", name=word)
        tx.create(leaf)

    ab = Relationship(tree, "KNOWS", leaf)
    tx.create(ab)

    tx.commit()


if __name__ == '__main__':
    try:
        gs = Graph(host="192.168.0.210", port=7687, verify=False)

        for file_name in ['words_alpha.txt', 'corncob_lowercase.txt', 'top-3000.txt']:
            with open(f'{os.getcwd()}/paper/{file_name}', 'r') as r:
                for word in r.readlines():
                    word = word.replace('\n', '').strip()
                    wtr = WordToRoot(word)
                    root = wtr.run()
                    if root and word != root:
                        save_to_neo4j(gs, word, root)

    except Exception as e:
        print(e)
