"""Limpieza, representaciones clásicas y Word2Vec de la muestra de Neuromante del curso."""
from pathlib import Path
import json
import unicodedata
import numpy as np
import spacy
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import PCA
from scipy.sparse import save_npz
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from adjustText import adjust_text

ROOT = Path(__file__).resolve().parent

def normalizar(doc):
    # Conservar negaciones: su eliminación puede cambiar el significado.
    conservar = {'no', 'nunca', 'jamás', 'sin'}
    return [lema for t in doc if t.is_alpha and
            (not t.is_stop or t.lower_ in conservar)
            for lema in t.lemma_.lower().split() if lema]

def visualizar(vectores, palabras, titulo, archivo):
    coords = PCA(n_components=2, random_state=42).fit_transform(vectores)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(coords[:, 0], coords[:, 1], c='#246b9e', s=35)
    texts = [ax.text(xy[0], xy[1], palabra, fontsize=9) for xy, palabra in zip(coords, palabras)]
    adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle='-', color='gray', lw=.5), ensure_inside_axes=True)
    ax.set(title=titulo, xlabel='Componente principal 1', ylabel='Componente principal 2')
    ax.text(0, -0.13, 'PCA es una proyección: las distancias 2D no preservan toda la información.',
            transform=ax.transAxes, fontsize=9)
    fig.tight_layout(); fig.savefig(archivo, dpi=160); plt.close(fig)

def main():
    out = ROOT / 'resultados'; out.mkdir(exist_ok=True)
    text = unicodedata.normalize('NFC', (ROOT/'data/neuromante_muestra.txt').read_text(encoding='utf-8'))
    nlp = spacy.load('es_core_news_sm', disable=['ner'])
    doc = nlp(text)
    sentences = [normalizar(s) for s in doc.sents]
    sentences = [s for s in sentences if s]
    corpus = [' '.join(s) for s in sentences]
    (out/'texto_procesado.txt').write_text('\n'.join(corpus), encoding='utf-8')
    rows = [{'original':t.text,'lema':t.lemma_.lower(),'stopword':t.is_stop} for t in doc if t.is_alpha]
    (out/'tokens.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    count = CountVectorizer(token_pattern=r'(?u)\b\w+\b')
    tfidf = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b')
    bow = count.fit_transform(corpus); weights = tfidf.fit_transform(corpus)
    save_npz(out/'bow.npz', bow); save_npz(out/'tfidf.npz', weights)
    words = tfidf.get_feature_names_out()
    (out/'vocabulario.json').write_text(json.dumps(words.tolist(),ensure_ascii=False),encoding='utf-8')
    # Un trabajador y semilla fija facilitan reproducibilidad.
    model = Word2Vec(sentences=sentences, vector_size=30, window=4,
                     min_count=1, sg=1, workers=1, seed=42, epochs=150)
    model.save(str(out/'word2vec.model'))
    frequent = sorted(range(len(words)), key=lambda i: (-float(bow[:,i].sum()), words[i]))[:25]
    selected = [words[i] for i in frequent]
    visualizar(weights[:,frequent].T.toarray(), selected,
               'TF-IDF del fragmento oficial de Neuromante (25 términos)', out/'espacio_tfidf.png')
    visualizar(np.array([model.wv[w] for w in selected]), selected,
               'Word2Vec Skip-gram de la muestra de Neuromante (30D a 2D)', out/'espacio_word2vec.png')
    query = 'case' if 'case' in model.wv else model.wv.index_to_key[0]
    summary = {'consulta':query,'oraciones':len(corpus),'tokens_originales':len(doc),'tokens_limpios':sum(map(len,sentences)),
               'vocabulario':len(words),'forma_bow':list(bow.shape),'forma_tfidf':list(weights.shape),
               'similares_consulta':model.wv.most_similar(query,topn=5),
               'limitacion':'Muestra de una sola obra: similitudes exploratorias, sin validación semántica independiente.'}
    (out/'resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
