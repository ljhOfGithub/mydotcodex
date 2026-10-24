#!/usr/bin/env python3
"""Generate candidate CET-6+ vocabulary from paper text files.

This is a heuristic candidate extractor. It intentionally favors recall; the
agent using the skill should review, translate, and polish the final glossary.
"""

from __future__ import annotations

import argparse
import collections
import html
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Iterable


SUPPORTED_SUFFIXES = {".txt", ".md", ".markdown", ".pdf", ".docx"}
SKIP_DIR_NAMES = {".git", ".pytest_cache", "__pycache__", "node_modules", "skills"}
SKIP_FILE_NAMES = {
    "README.md", "README.en.md", "requirements.txt",
    "Paper_Reader.template.txt", "Paper_Reader.template.en.txt",
}
SKIP_FILE_PATTERNS = (
    re.compile(r"cet[46]-plus-vocab-.*\.md$", re.IGNORECASE),
)

BASIC_WORDS = {
    "a", "able", "about", "above", "accept", "according", "account", "across",
    "act", "action", "activity", "add", "after", "again", "against", "age",
    "ago", "agree", "air", "all", "allow", "almost", "alone", "along",
    "already", "also", "although", "always", "among", "an", "and", "animal",
    "another", "answer", "any", "anyone", "anything", "appear", "area", "arm",
    "around", "arrive", "art", "as", "ask", "at", "away", "back", "bad",
    "bag", "base", "basic", "be", "bear", "beat", "beautiful", "because",
    "become", "bed", "before", "begin", "behind", "believe", "best",
    "better", "between", "big", "bird", "black", "blue", "body", "book",
    "both", "box", "boy", "break", "bring", "brother", "build", "business",
    "but", "buy", "by", "call", "can", "capital", "car", "care", "case",
    "center", "certain", "change", "check", "child", "city", "class",
    "clear", "close", "cold", "come", "common", "company", "computer",
    "condition", "consider", "control", "course", "create", "current", "cut",
    "data", "day", "decide", "develop", "different", "difficult", "do",
    "door", "down", "during", "each", "early", "earth", "easy", "eat",
    "education", "effect", "end", "enough", "even", "ever", "every",
    "example", "eye", "face", "fact", "family", "far", "father", "feel",
    "few", "field", "find", "first", "five", "follow", "food", "for",
    "form", "four", "free", "friend", "from", "full", "game", "get",
    "girl", "give", "go", "good", "great", "green", "group", "grow", "hand",
    "happen", "hard", "has", "have", "he", "head", "hear", "help", "her",
    "here", "high", "him", "his", "history", "home", "hot", "hour", "house",
    "how", "however", "human", "idea", "if", "important", "in", "include",
    "increase", "interest", "into", "is", "it", "its", "job", "just",
    "keep", "kind", "know", "large", "last", "late", "learn", "leave",
    "left", "less", "let", "level", "life", "light", "like", "line",
    "little", "live", "long", "look", "lot", "low", "make", "man", "many",
    "may", "mean", "meet", "member", "method", "might", "minute", "money",
    "more", "morning", "most", "mother", "move", "much", "must", "name",
    "near", "need", "never", "new", "next", "night", "no", "not", "note",
    "now", "number", "of", "off", "often", "old", "on", "once", "one",
    "only", "open", "or", "order", "other", "our", "out", "over", "own",
    "paper", "part", "people", "person", "place", "plan", "play", "point",
    "possible", "power", "problem", "process", "provide", "public", "put",
    "question", "quick", "read", "real", "reason", "red", "result", "right",
    "room", "run", "same", "say", "school", "science", "second", "see",
    "seem", "sentence", "set", "she", "short", "should", "show", "side",
    "small", "so", "some", "something", "sound", "start", "state", "still",
    "stop", "study", "student", "such", "system", "table", "take", "talk",
    "team", "tell", "than", "that", "the", "their", "them", "then", "there",
    "these", "they", "thing", "think", "this", "those", "three", "through",
    "time", "to", "today", "together", "too", "try", "two", "under",
    "understand", "up", "us", "use", "user", "very", "want", "war", "water",
    "way", "we", "week", "well", "were", "what", "when", "where", "which",
    "while", "white", "who", "why", "will", "with", "without", "woman",
    "word", "work", "world", "would", "write", "year", "yes", "you", "young",
    "your",
}

ACADEMIC_KEEP_HINTS = {
    "ablation", "algorithmic", "alignment", "annotation", "architecture",
    "augmentation", "benchmark", "causal", "coherence", "convergence",
    "corpus", "decomposition", "diffusion", "embedding", "empirical",
    "fine-tuning", "granular", "hallucination", "inference", "latent",
    "mitigate", "modality", "optimization", "paradigm", "representation",
    "retrieval", "robustness", "semantic", "stochastic", "supervised",
    "synthetic", "taxonomy", "trajectory", "unsupervised", "adversarial",
    "calibration", "conformance", "elicitation", "heterogeneity",
    "interoperability", "orchestration", "provenance", "quantization",
    "scalability", "sparsification", "throughput",
}

CET6_OR_TOO_COMMON = {
    "ability", "academic", "additional", "application", "applications",
    "background", "capabilities", "challenge", "challenges", "communication",
    "conference", "conferences", "considered", "development", "different",
    "discussion", "effective", "efficiently", "engineering", "environment",
    "evaluation", "evidence", "explanation", "information", "international",
    "literature", "management", "particular", "performance", "presentation",
    "presentations", "previous", "professional", "recommendation",
    "recommended", "reference", "references", "relation", "requirements",
    "research", "significant", "significantly", "technology", "university",
    "various", "construction", "creative", "environmental", "examination",
    "indicative", "innovative", "methodologies", "preparation",
    "productivity", "technologies", "transportation", "understanding",
}

CHINESE_MEANINGS = {
    "ablation": "消融；消融实验",
    "adversarial": "对抗性的；用于攻击或鲁棒性测试的",
    "alignment": "对齐；与人类偏好或目标保持一致",
    "annotation": "标注；注释",
    "architecture": "架构；体系结构",
    "architectures": "架构；体系结构",
    "augmentation": "增强；数据增强",
    "appropriateness": "适切性；合适程度",
    "association": "关联；联合；用户关联",
    "audience": "受众；听众",
    "automation": "自动化",
    "benchmark": "基准测试；评测基准",
    "calibration": "校准；概率或仪器校准",
    "capability": "能力；系统可完成任务的能力",
    "characteristics": "特征；性质",
    "classification": "分类",
    "causal": "因果的",
    "coherence": "连贯性；一致性",
    "collaboration": "协作；合作",
    "combination": "组合；结合",
    "communicative": "交际的；通信的",
    "communications": "通信；通讯",
    "competence": "胜任力；能力",
    "comprehensive": "综合的；全面的",
    "computation": "计算；计算过程",
    "computational": "计算的；计算相关的",
    "conformance": "符合性；合规一致性",
    "convergence": "收敛",
    "corresponding": "相应的；对应的",
    "corpus": "语料库；文本集合",
    "decomposition": "分解；拆解",
    "departmental": "院系的；部门的",
    "difference": "差异；不同点",
    "diffusion": "扩散；扩散模型中的逐步生成过程",
    "disciplinary": "学科的；学科领域内的",
    "dissertation": "学位论文；博士论文",
    "distribution": "分布；分发；系统部署分布",
    "distributions": "分布；发行版；部署版本",
    "elicitation": "诱导；引出；偏好/偏差诱发",
    "embedding": "嵌入；向量表示",
    "embeddings": "嵌入向量；向量表示",
    "empirical": "实证的；基于实验观察的",
    "environments": "环境；运行环境",
    "epistemological": "认识论的；关于知识来源和有效性的",
    "excellence": "卓越；优秀",
    "experimental": "实验性的；基于实验的",
    "effectiveness": "有效性",
    "efficiency": "效率；资源利用效率",
    "fine-tuning": "微调",
    "foundation": "基础；基础模型语境中的底座",
    "frequency": "频率",
    "generation": "生成；生成过程",
    "generative": "生成式的",
    "geotechnical": "岩土工程的",
    "granular": "细粒度的",
    "hallucination": "幻觉；模型编造内容",
    "heterogeneity": "异构性；差异性",
    "identification": "识别；辨识",
    "implication": "含义；影响；启示",
    "implications": "含义；影响；启示",
    "implementation": "实现；实施",
    "infrastructure": "基础设施",
    "inference": "推理；模型推断",
    "influence": "影响；作用",
    "integration": "集成；整合",
    "intelligence": "智能；智能系统能力",
    "interactions": "交互；相互作用",
    "interoperability": "互操作性；跨系统协同能力",
    "instructions": "指令；任务说明",
    "latent": "潜在的；隐变量空间中的",
    "linguistic": "语言学的；语言层面的",
    "logistic": "逻辑斯蒂的；后勤/逻辑相关的",
    "mitigate": "缓解；减轻",
    "mitigation": "缓解；减轻措施",
    "modality": "模态；数据类型",
    "methodology": "方法论；研究方法",
    "navigation": "导航；路径/网页浏览任务",
    "observation": "观察；观测结果",
    "observations": "观察；观测结果",
    "operation": "操作；运行过程",
    "opportunities": "机会；研究机会",
    "optimization": "优化",
    "orchestration": "编排；多组件调度协调",
    "orientation": "导向；开场引入；方向定位",
    "paradigm": "范式；基本研究/设计模式",
    "participants": "参与者；受试者",
    "particularly": "尤其；特别地",
    "postgraduate": "研究生的；研究生",
    "probability": "概率",
    "publication": "出版物；发表",
    "publications": "出版物；发表成果",
    "provenance": "来源；数据血缘；出处追踪",
    "quantization": "量化；降低数值精度以压缩模型",
    "quantitative": "定量的",
    "reconstruction": "重建；复原",
    "reconstructed": "被重建的；复原后的",
    "reinforcement": "强化；强化学习语境中的奖励驱动学习",
    "relationship": "关系；关联",
    "relative": "相对的",
    "reliability": "可靠性",
    "representation": "表示；表征",
    "representations": "表示；表征",
    "resilience": "韧性；恢复能力",
    "respectively": "分别地；各自地",
    "retrieval": "检索",
    "robustness": "鲁棒性；抗干扰能力",
    "satisfaction": "满足；满意度；约束满足",
    "scalability": "可扩展性",
    "scheduling": "调度；资源安排",
    "semantic": "语义的",
    "sequence": "序列；顺序",
    "significance": "显著性；重要性",
    "simulation": "仿真；模拟",
    "sparsification": "稀疏化",
    "specifically": "具体而言；特别地",
    "statistically": "统计上地",
    "stochastic": "随机的；概率性的",
    "suitability": "适合性；适配程度",
    "sustainability": "可持续性",
    "supervised": "有监督的",
    "synthetic": "合成的；人工生成的",
    "taxonomy": "分类体系；分类法",
    "termination": "终止；结束；结尾收束",
    "throughput": "吞吐量",
    "transactions": "事务；交易；期刊名语境中为 Transactions",
    "trajectory": "轨迹；行动序列",
    "trajectories": "轨迹；行动序列",
    "uncertainty": "不确定性",
    "uncertainties": "不确定性；误差来源",
    "unsupervised": "无监督的",
    "variation": "变异；差异变化",
}

PHRASE_MEANINGS = {
    "artificial intelligence": "人工智能",
    "background estimation": "背景估计",
    "causal inference": "因果推断",
    "comprehensive evaluation": "综合评估",
    "computation offloading": "计算卸载",
    "computational complexity": "计算复杂度",
    "computational efficiency": "计算效率",
    "computational linguistics": "计算语言学",
    "compression techniques": "压缩技术",
    "inference latency": "推理延迟",
    "information processing": "信息处理",
    "latent representation": "潜在表示；隐空间表征",
    "multi-agent collaboration": "多智能体协作",
    "multi-agent reinforcement": "多智能体强化学习",
    "optimization techniques": "优化技术",
    "performance comparison": "性能对比",
    "performance evaluation": "性能评估",
    "real-world applications": "真实世界应用",
    "reconstruction algorithms": "重建算法",
    "sensitive information": "敏感信息",
    "statistical significance": "统计显著性",
    "statistical uncertainty": "统计不确定性",
    "systematic uncertainty": "系统性不确定性",
    "systematic uncertainties": "系统性不确定性",
}


def iter_files(path: Path) -> list[Path]:
    root = path if path.is_dir() else path.parent

    def should_skip(p: Path) -> bool:
        try:
            rel_parts = p.relative_to(root).parts
        except ValueError:
            rel_parts = p.parts
        if any(part in SKIP_DIR_NAMES for part in rel_parts[:-1]):
            return True
        if p.name in SKIP_FILE_NAMES:
            return True
        return any(pattern.match(p.name) for pattern in SKIP_FILE_PATTERNS)

    if path.is_file():
        return [path] if path.suffix.lower() in SUPPORTED_SUFFIXES and not should_skip(path) else []
    return sorted(
        p for p in path.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES and not should_skip(p)
    )


def read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        chunks = []
        for name in zf.namelist():
            if name.startswith("word/") and name.endswith(".xml"):
                text = zf.read(name).decode("utf-8", errors="ignore")
                text = re.sub(r"<[^>]+>", " ", text)
                chunks.append(html.unescape(text))
        return "\n".join(chunks)


def read_pdf(path: Path) -> str:
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return ""


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return read_pdf(path)
    if suffix == ".docx":
        return read_docx(path)
    return path.read_text(encoding="utf-8", errors="ignore")


def normalize_token(token: str) -> str:
    token = token.lower().strip("'")
    token = re.sub(r"'s$", "", token)
    return token


def translate_item(item: str) -> str:
    if item in PHRASE_MEANINGS:
        return PHRASE_MEANINGS[item]
    if item in CHINESE_MEANINGS:
        return CHINESE_MEANINGS[item]
    if item.endswith("s") and item[:-1] in CHINESE_MEANINGS:
        return CHINESE_MEANINGS[item[:-1]]
    return "需结合上下文确认"


def likely_cet6_plus(word: str) -> bool:
    if len(word) < 8:
        return False
    if word in BASIC_WORDS:
        return False
    if word in CET6_OR_TOO_COMMON:
        return False
    if any(ch.isdigit() for ch in word):
        return False
    if "-" in word and word not in ACADEMIC_KEEP_HINTS:
        return False
    if word in ACADEMIC_KEEP_HINTS:
        return True
    if len(word) >= 12:
        return True
    academic_suffixes = (
        "ability", "ation", "ative", "ence", "ency", "istic",
        "ization", "ology",
    )
    return word.endswith(academic_suffixes)


def token_contexts(text: str, word: str, limit: int = 2) -> list[str]:
    contexts = []
    pattern = re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
    for match in pattern.finditer(text):
        start = max(0, match.start() - 70)
        end = min(len(text), match.end() + 70)
        snippet = re.sub(r"\s+", " ", text[start:end]).strip()
        contexts.append(snippet)
        if len(contexts) >= limit:
            break
    return contexts


def extract_words(texts: dict[Path, str]) -> tuple[collections.Counter[str], dict[str, set[Path]]]:
    counts: collections.Counter[str] = collections.Counter()
    sources: dict[str, set[Path]] = collections.defaultdict(set)
    for path, text in texts.items():
        for raw in re.findall(r"[A-Za-z][A-Za-z'-]*[A-Za-z]", text):
            word = normalize_token(raw)
            if likely_cet6_plus(word):
                counts[word] += 1
                sources[word].add(path)
    return counts, sources


def extract_phrases(texts: dict[Path, str], valid_words: set[str]) -> collections.Counter[str]:
    phrases: collections.Counter[str] = collections.Counter()
    for text in texts.values():
        tokens = [normalize_token(t) for t in re.findall(r"[A-Za-z][A-Za-z'-]*[A-Za-z]", text)]
        for first, second in zip(tokens, tokens[1:]):
            if first in valid_words and second in valid_words:
                phrases[f"{first} {second}"] += 1
    return phrases


def render_markdown(
    input_path: Path,
    texts: dict[Path, str],
    counts: collections.Counter[str],
    sources: dict[str, set[Path]],
    top: int,
    min_count: int,
    include_phrases: bool,
) -> str:
    filtered = [(word, count) for word, count in counts.most_common() if count >= min_count][:top]
    source_lines = "\n".join(f"- {path}" for path in texts)
    lines = [
        "# CET-6+ 论文词表候选",
        "",
        "来源:",
        source_lines or f"- {input_path}",
        "",
        "证据等级: 全文候选；请结合论文语境人工复核",
        "",
        "| Word / Phrase | 中文含义 | 论文语境 | 难度原因 | 出现次数 | 来源 |",
        "|---|---|---|---|---:|---|",
    ]
    combined_text = "\n".join(texts.values())
    for word, count in filtered:
        contexts = token_contexts(combined_text, word, limit=1)
        context = contexts[0] if contexts else ""
        reason = "长度/学术后缀/论文常用术语提示为 CET-6+ 候选"
        if word in ACADEMIC_KEEP_HINTS:
            reason = "学术论文专门术语，通常超出 CET-6 常规词汇"
        src = "; ".join(str(p) for p in sorted(sources[word]))
        lines.append(f"| {word} | {translate_item(word)} | {context} | {reason} | {count} | {src} |")

    if include_phrases:
        phrase_counts = extract_phrases(texts, {word for word, _ in filtered})
        common_phrases = [(p, c) for p, c in phrase_counts.most_common(30) if c >= min_count]
        if common_phrases:
            lines.extend(["", "## 高频学术短语候选", "", "| Phrase | 中文含义 | 出现次数 |", "|---|---|---:|"])
            for phrase, count in common_phrases:
                lines.append(f"| {phrase} | {translate_item(phrase)} | {count} |")
    return "\n".join(lines) + "\n"


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract candidate CET-6+ vocabulary from paper files.")
    parser.add_argument("--input", required=True, help="Input file or folder.")
    parser.add_argument("--output", help="Output Markdown path. Defaults to stdout.")
    parser.add_argument("--top", type=int, default=120, help="Maximum candidate words.")
    parser.add_argument("--min-count", type=int, default=1, help="Minimum frequency.")
    parser.add_argument("--include-phrases", action="store_true", help="Include frequent academic bigrams.")
    args = parser.parse_args(argv)

    input_path = Path(args.input).expanduser().resolve()
    files = iter_files(input_path)
    if not files:
        print(f"No supported files found under {input_path}", file=sys.stderr)
        return 2

    texts = {path: read_text(path) for path in files}
    texts = {path: text for path, text in texts.items() if text.strip()}
    if not texts:
        print("No readable text extracted. PDF may need OCR.", file=sys.stderr)
        return 3

    counts, sources = extract_words(texts)
    markdown = render_markdown(
        input_path=input_path,
        texts=texts,
        counts=counts,
        sources=sources,
        top=args.top,
        min_count=args.min_count,
        include_phrases=args.include_phrases,
    )
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
