# MediScope AI Dataset Cards

## 1. Retinal Fundus Dataset (APTOS 2019 & Messidor Subset)
- **Source:** APTOS 2019 Blindness Detection / Messidor Consortium.
- **License:** CC BY-NC-SA 4.0 (Research & Educational Use).
- **Usable Samples:** 3,662 annotated retinal fundus photographs.
- **Classes:** Normal (0), Mild/Moderate DR (1), Glaucoma Signs (2), Cataract (3), AMD (4).
- **Split Strategy:** Patient ID grouping (70% train / 15% val / 15% test).
- **Known Biases:** Imbalance towards mild diabetic retinopathy cases; photography illumination variation.

## 2. Chest Radiograph Dataset (NIH ChestX-ray14 & CheXpert Subset)
- **Source:** NIH Clinical Center ChestX-ray14 / Stanford CheXpert.
- **License:** Open Access Public Domain / Research License.
- **Usable Samples:** 10,000 frontal chest radiographs.
- **Classes:** Normal (0), Pneumonia (1), Tuberculosis Suspicion (2), Cardiomegaly (3), Effusion (4).
- **Split Strategy:** Patient-level split to prevent data leakage.

## 3. Bone Fracture Localization Dataset (GRAZPEDWRI & MURA)
- **Source:** GRAZPEDWRI Pediatric Radiography / Stanford MURA.
- **License:** Open Data Research License.
- **Usable Samples:** 4,200 annotated bone radiographs with bounding box coordinates.
- **Annotation Type:** YOLO Bounding Box Format (`class x_center y_center width height`).

## 4. PlantVillage Agricultural Crop Leaf Dataset
- **Source:** Penn State PlantVillage Dataset.
- **License:** CC0 Public Domain.
- **Usable Samples:** 8,000 crop leaf photos.
- **Classes:** Healthy Leaf, Bacterial Blight, Fungal Rust, Powdery Mildew, Leaf Spot.
