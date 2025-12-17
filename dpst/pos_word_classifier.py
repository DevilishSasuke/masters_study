import os
import re
import joblib
import numpy as np
import matplotlib.pyplot as plt

from datasets import load_dataset
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, f1_score

VOWELS = set("aeiouy")

# Universal Dependencies UPOS ids (as used by the HF dataset loader) -> tag string
UPOS_ID2TAG = {
    0: "NOUN",
    1: "PUNCT",
    2: "ADP",
    3: "NUM",
    4: "SYM",
    5: "SCONJ",
    6: "ADJ",
    7: "PART",
    8: "DET",
    9: "CCONJ",
    10: "PROPN",
    11: "PRON",
    12: "X",
    13: "ADV",
    14: "INTJ",
    15: "VERB",
    16: "AUX",
}


def load_ud_word_pos(
    language: str = "en",
    treebank: str = "ewt",
    keep_pos=("NOUN", "VERB", "ADJ"),
    max_rows: int | None = None,
    debug_preview: bool = False,
):
    """
    Load words and their UPOS tags from Universal Dependencies (HF datasets),
    then filter to desired POS tags and clean tokens.

    Returns:
        words: list[str]
        labels: list[str]
    """
    ds = load_dataset(
        "universal_dependencies",
        f"{language}_{treebank}",
        split="train",
        trust_remote_code=True,
    )

    if debug_preview:
        print(ds[0]["tokens"][:10])
        print(ds[0]["upos"][:10])

    words, labels = [], []

    for ex in ds:
        for w, upos_id in zip(ex["tokens"], ex["upos"]):
            if not w:
                continue

            w = str(w).strip().lower()

            # Convert numeric UPOS id -> tag string
            try:
                upos = UPOS_ID2TAG.get(int(upos_id))
            except Exception:
                upos = None

            if upos is None:
                continue

            if upos not in keep_pos:
                continue

            # keep only alphabetic words (drop punctuation, hyphenated tokens, etc.)
            if not w.isalpha():
                continue

            words.append(w)
            labels.append(upos)

            if max_rows and len(words) >= max_rows:
                return words, labels

    if len(words) == 0:
        raise ValueError(
            "No samples collected. Try a different treebank (e.g., treebank='gum' or 'lines'), "
            "or relax filtering (remove isalpha())."
        )

    return words, labels


def morph_features(words):
    """
    Convert a list/array of words to a numeric feature matrix using simple morphology features.
    """
    feats = []
    for w in words:
        length = len(w)
        vcount = sum(1 for ch in w if ch in VOWELS)
        vowel_ratio = vcount / length if length else 0.0

        feats.append([
            length,
            vcount,
            vowel_ratio,
            int(w.endswith("ly")),
            int(w.endswith("ing")),
            int(w.endswith("ed")),
            int(w.endswith("tion")),
            int(w.endswith("ment")),
            int(w.endswith("able")),
            int(w.endswith("ous")),
            int(w.endswith("ive")),
            int(w.endswith("ness")),
        ])

    return np.array(feats, dtype=float)


def plot_confusion(cm, labels, title="Confusion matrix"):
    plt.figure(figsize=(6, 5))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    ticks = np.arange(len(labels))
    plt.xticks(ticks, labels, rotation=45, ha="right")
    plt.yticks(ticks, labels)

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(
                j,
                i,
                str(cm[i, j]),
                ha="center",
                va="center",
                color="white" if cm[i, j] > cm.max() / 2 else "black",
            )

    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()
    plt.show()


def main():
    OUT_DIR = "output_pos_word_classifier"
    os.makedirs(OUT_DIR, exist_ok=True)

    LABELS_ORDER = ["NOUN", "VERB", "ADJ"]

    print("Loading dataset...")
    X, y = load_ud_word_pos(
        keep_pos=tuple(LABELS_ORDER),
        max_rows=60000,
        debug_preview=False,  # set True if you want to preview tokens/upos again
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ----------------------------
    # Build pipelines (one per model)
    # ----------------------------

    # Linear SVM pipeline: n-grams + morphology
    ngram_block = ("ngram", TfidfVectorizer(analyzer="char", ngram_range=(2, 4), min_df=2))
    morph_block = ("morph", Pipeline([
        ("extract", FunctionTransformer(morph_features, validate=False)),
        ("scale", StandardScaler()),
    ]))
    features_full = FeatureUnion([ngram_block, morph_block])

    svm_pipe = Pipeline([
        ("features", features_full),
        ("clf", LinearSVC(max_iter=20000, tol=1e-3)),
    ])

    # Naive Bayes pipeline: n-grams ONLY (must be non-negative)
    nb_pipe = Pipeline([
        ("ngram", TfidfVectorizer(analyzer="char", ngram_range=(2, 4), min_df=2)),
        ("clf", MultinomialNB()),
    ])

    model_specs = [
        {
            "name": "linear_svm",
            "pipe": svm_pipe,
            "param_grid": {
                "clf__C": [0.5, 1, 2, 5],
                "features__ngram__ngram_range": [(2, 4), (3, 5)],
                "features__ngram__min_df": [2, 5],
            },
        },
        {
            "name": "naive_bayes",
            "pipe": nb_pipe,
            "param_grid": {
                "ngram__ngram_range": [(2, 4), (3, 5)],
                "ngram__min_df": [2, 5],
                "clf__alpha": [0.1, 0.5, 1.0],
            },
        },
    ]

    best_overall_estimator = None
    best_overall_name = None
    best_overall_macro_f1 = -1.0

    # ----------------------------
    # Training loop
    # ----------------------------
    for spec in model_specs:
        name = spec["name"]
        pipe = spec["pipe"]
        param_grid = spec["param_grid"]

        print(f"\nTraining model: {name}")
        grid = GridSearchCV(
            pipe,
            param_grid,
            cv=3,
            n_jobs=-1,
            verbose=2,          # prints progress
            error_score="raise" # easier debugging if something fails
        )

        grid.fit(X_train, y_train)

        print("Best params:", grid.best_params_)
        print("Best CV score:", grid.best_score_)

        y_pred = grid.predict(X_test)

        macro_f1 = f1_score(y_test, y_pred, average="macro")
        micro_f1 = f1_score(y_test, y_pred, average="micro")

        print(f"Test macro F1: {macro_f1:.4f}")
        print(f"Test micro F1: {micro_f1:.4f}")
        print(classification_report(y_test, y_pred, digits=4))

        cm = confusion_matrix(y_test, y_pred, labels=LABELS_ORDER)
        plot_confusion(cm, LABELS_ORDER, title=f"Confusion matrix - {name}")

        if macro_f1 > best_overall_macro_f1:
            best_overall_macro_f1 = macro_f1
            best_overall_estimator = grid.best_estimator_
            best_overall_name = name

    # ----------------------------
    # Save best overall model
    # ----------------------------
    model_path = os.path.join(OUT_DIR, f"best_model_{best_overall_name}.joblib")
    joblib.dump(best_overall_estimator, model_path)

    print(f"\nSaved best overall model to: {model_path}")
    print(f"Best overall macro F1: {best_overall_macro_f1:.4f}")


if __name__ == "__main__":
    main()
