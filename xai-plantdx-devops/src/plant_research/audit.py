from pathlib import Path
from collections import Counter
import argparse, json

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
SPLIT_NAMES = {"train", "validation", "valid", "val", "test"}

def discover_images(root: Path) -> list[Path]:
    root = Path(root)
    if not root.exists():
        raise FileNotFoundError(f"Dataset directory does not exist: {root}")
    return sorted((p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS),
                  key=lambda p: p.as_posix().lower())

def audit_dataset(root: Path) -> dict:
    root = Path(root)
    images = discover_images(root)
    if not images:
        raise ValueError(f"No supported image files found under: {root}")
    top = [p.name.lower() for p in root.iterdir() if p.is_dir()]
    has_splits = any(x in SPLIT_NAMES for x in top)
    counts, names = {}, Counter()
    for image in images:
        parts = image.relative_to(root).parts
        if has_splits and len(parts) >= 3 and parts[0].lower() in SPLIT_NAMES:
            split, cls = parts[0].lower(), parts[1]
        elif len(parts) >= 2:
            split, cls = "all", parts[0]
        else:
            split, cls = "unlabelled", "unlabelled"
        counts.setdefault(split, Counter())[cls] += 1
        names[image.name.lower()] += 1
    classes = sorted({c for counter in counts.values() for c in counter})
    repeated = sorted(n for n, count in names.items() if count > 1)
    warnings = []
    if len(classes) < 2: warnings.append("Fewer than two classes were detected; verify the folder layout.")
    if repeated: warnings.append(f"{len(repeated)} filename(s) occur more than once; inspect possible duplicates.")
    splits = {s: {"total": sum(c.values()), "classes": dict(sorted(c.items()))} for s,c in sorted(counts.items())}
    return {"dataset_root": str(root.resolve()), "image_count": len(images), "class_names": classes,
            "splits": splits, "repeated_filenames": repeated, "warnings": warnings}

def main():
    parser = argparse.ArgumentParser(description="Audit a plant disease image dataset.")
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try: report = audit_dataset(args.dataset)
    except (FileNotFoundError, ValueError) as exc: parser.error(str(exc))
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\\n", encoding="utf-8")
    print(text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
