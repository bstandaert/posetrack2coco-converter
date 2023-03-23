import os
import cv2
import glob
import json
from tqdm import tqdm
import argparse


def handle_args():
    parser = argparse.ArgumentParser(
        prog="main.py", description="Convert posetrack to coco format"
    )
    parser.add_argument(
        "--annotation-path",
        type=str,
        required=True,
        help="Path to annotation directory",
    )
    parser.add_argument(
        "--data-path", type=str, required=True, help="Path to data directory"
    )
    parser.add_argument(
        "--output-path", type=str, required=True, help="Path to output directory"
    )
    return parser.parse_args()


def get_image_shape(image_path):
    """
    Get the shape of an image
    :param image_path: path to image
    :return: list of 2 ints (width, height)
    """
    image = cv2.imread(image_path)
    return image.shape[1], image.shape[0]


def generate_split(output_file, data_path, annotation_files):
    """
    Generate a split file for the dataset
    :param output_file: path to output file
    :param data_path: path to data directory
    :param annotation_files: list of paths to annotations
    """
    images = []
    annotations = []
    for annotation_file in tqdm(annotation_files):
        with open(annotation_file, "r") as f:
            ann_dict = json.load(f)

        ann_images = ann_dict["images"]
        image_shape = get_image_shape(
            os.path.join(data_path, ann_images[0]["file_name"])
        )
        for ann_image in ann_images:
            ann_image["has_no_densepose"] = True
            ann_image["width"] = image_shape[0]
            ann_image["height"] = image_shape[1]
            if "image_id" in ann_image:  # check if needed ?
                ann_image["frame_id"] = ann_image.pop("image_id")
            #if "has_labeled_person" in ann_image:  # check if needed ?
            #    ann_image.pop("has_labeled_person")
        images.extend(ann_images)

        ann_annotations = ann_dict["annotations"]
        for ann_annotation in ann_annotations:
            ann_annotation["iscrowd"] = False
            ann_annotation["num_keypoints"] = int(
                sum(ann_annotation["keypoints"][2::3])
            )
            ann_annotation["scores"] = []
            ann_annotation["segmentation"] = []
            if "bbox" in ann_annotation:
                bbox_w, bbow_h = ann_annotation["bbox"][2:]
                ann_annotation["area"] = bbox_w * bbow_h
            #if "person_id" in ann_annotation:  # check if needed ?
            #    ann_annotation.pop("person_id")
            #if "track_id" in ann_annotation:  # check if needed ?
            #    ann_annotation.pop("track_id")
        annotations.extend(ann_annotations)
    categories = ann_dict["categories"]
    with open(output_file, "w") as f:
        json.dump(
            {"images": images, "annotations": annotations, "categories": categories}, f, indent=4
        )


def main():
    args = handle_args()

    train_anns_path = os.path.join(args.annotation_path, "train")
    val_anns_path = os.path.join(args.annotation_path, "val")
    test_anns_path = os.path.join(args.annotation_path, "test")
    data_path = args.data_path

    train_anns = glob.glob(os.path.join(train_anns_path, "*.json"))
    val_anns = glob.glob(os.path.join(val_anns_path, "*.json"))
    test_anns = glob.glob(os.path.join(test_anns_path, "*.json"))

    assert len(train_anns) > 0, "No training annotations found"
    assert len(val_anns) > 0, "No validation annotations found"
    output_dir = args.output_path
    os.makedirs(output_dir, exist_ok=True)
    generate_split(os.path.join(output_dir, "posetrack_train.json"), data_path, train_anns)
    generate_split(os.path.join(output_dir, "posetrack_val.json"), data_path, val_anns)
    try:
        generate_split(os.path.join(output_dir, "posetrack_test.json"), data_path, test_anns)
    except:
        print("No test annotations found")


if __name__ == "__main__":
    main()
