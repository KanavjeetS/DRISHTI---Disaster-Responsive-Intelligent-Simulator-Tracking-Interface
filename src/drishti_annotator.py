from ultralytics import YOLO
from pathlib import Path
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import os

MODEL = "yolo11n.pt"
CONFIDENCE = 0.25
IMG_SIZE = 640
IMG_EXTS = {'.jpg','.jpeg','.png','.bmp','.tiff'}

print("Loading model:", MODEL)
model = YOLO(MODEL)
print("Model loaded. Model knows these classes:", model.names)


def annotate_folder(folder_path: str, conf: float = CONFIDENCE, imgsz: int = IMG_SIZE):
    """Annotate all images in folder_path using yolo11n.
    Creates two subfolders inside folder_path:
      - annotated/      (annotated images saved as same filename)
      - annotations/    (YOLO-format .txt files, one per image)
    Returns (annotated_dir, ann_dir)
    """
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Not a folder: {folder_path}")

    annotated_dir = folder / "annotated_valid"
    ann_dir = folder / "annotations_valid"
    annotated_dir.mkdir(exist_ok=True)
    ann_dir.mkdir(exist_ok=True)

    imgs = [p for p in sorted(folder.iterdir()) if p.suffix.lower() in IMG_EXTS]
    if len(imgs) == 0:
        print("No images found in", folder)
        return annotated_dir, ann_dir

    for img_path in imgs:
        print("Processing:", img_path.name)
        results = model.predict(source=str(img_path), conf=conf, imgsz=imgsz, verbose=False)
        res = results[0] 
        im = Image.open(img_path)
        width, height = im.size

        yolo_lines = []
        boxes = getattr(res, 'boxes', None)

        if boxes is not None and len(boxes) > 0:

            try:
                xyxyn = boxes.xyxyn.cpu().numpy()
                cls_ids = boxes.cls.cpu().numpy().astype(int)
                confs = boxes.conf.cpu().numpy()
            except Exception:

                xyxy = boxes.xyxy.cpu().numpy()
                cls_ids = boxes.cls.cpu().numpy().astype(int)
                confs = boxes.conf.cpu().numpy()
                xyxyn = xyxy.copy()
                xyxyn[:, [0,2]] /= width
                xyxyn[:, [1,3]] /= height

            for (xmin, ymin, xmax, ymax), cls_id, conf_score in zip(xyxyn, cls_ids, confs):

                xmin = float(max(0.0, min(1.0, xmin)))
                ymin = float(max(0.0, min(1.0, ymin)))
                xmax = float(max(0.0, min(1.0, xmax)))
                ymax = float(max(0.0, min(1.0, ymax)))

                x_center = (xmin + xmax) / 2.0
                y_center = (ymin + ymax) / 2.0
                w_box = xmax - xmin
                h_box = ymax - ymin

                yolo_lines.append(f"{int(cls_id)} {x_center:.6f} {y_center:.6f} {w_box:.6f} {h_box:.6f}")

        txt_path = ann_dir / (img_path.stem + '.txt')
        with open(txt_path, 'w') as f:
            f.write('\n'.join(yolo_lines))

        try:
            ann_img = res.plot()  
            Image.fromarray(ann_img).save(annotated_dir / img_path.name)
        except Exception as e:
            print("Warning: could not plot result for", img_path.name, "- saving original. Error:", e)
            im.save(annotated_dir / img_path.name)

    print("Finished. Annotated images ->", annotated_dir)
    print("YOLO txts ->", ann_dir)
    return annotated_dir, ann_dir


def pick_folder_and_annotate():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title='Select images folder to annotate (will create annotated/ and annotations/)')
    if not folder:
        print('No folder selected.')
        return
    try:
        annotate_folder(folder)
        messagebox.showinfo('Done', f'Annotated images and YOLO txts saved inside:\n{folder}')
    except Exception as e:
        messagebox.showerror('Error', str(e))
