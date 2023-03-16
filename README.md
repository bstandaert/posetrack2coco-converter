# posetrack2yolo-converter
Convert your `PoseTrack18` or `PoseTrack21` annotations to `COCO` annotations to train your own models on a detection task.

## Installation
```bash
git clone https://github.com/bstandaert/posetrack2coco-converter.git
cd posetrack2coco-converter
pip install -r requirements.txt
```

## Usage
```bash
python main.py --annotation-path /path/to/annotations --data-path /path/to/data --output-path /path/to/output
```

### Expected annotation directory structure

```text
/path/to/annotations
├── train
│   └── *.json
├── val
│   └── *.json
└── test
    └── *.json
```

### Expected data directory structure

```text
/path/to/data
└── images
    ├── test
    │   ├── <video_name>
    │   │   └── *.jpg
    │   └── ...
    ├── train
    │   ├── <video_name>
    │   │   └── *.jpg
    │   └── ...
    └── val
        ├── <video_name>
        │   └── *.jpg
        └── ...
```

### Output directory structure

The script will create a `COCO` annotation file for each split in the `output-path` directory.
This is done by adaptating the `PoseTrack` annotation format to the `COCO` format and then by concatenating all the 
annotations into a single file. The test folder is ignored if not present.

```text
/path/to/output
├── posetrack_val.json
├── posetrack_train.json
└── posetrack_test.json
```

### Output file example

```text
{
    "images": [
        {
            "has_no_densepose": true,
            "is_labeled": true,
            "file_name": "images/val/000342_mpii_test/000000.jpg",
            "nframes": 100,
            "frame_id": 10003420000,
            "vid_id": "000342",
            "id": 10003420000,
            "width": 854,
            "height": 480
        },
        ...
    ],
    "annotations": [
        ...,
        {
            "bbox_head": [
                564,
                139,
                69,
                92
            ],
            "keypoints": [
                608,
                198.5,
                1,
                561.7000122,
                212.6000061,
                1,
                626.0999756,
                164.3000031,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                558,
                185.5,
                1,
                547,
                253.5,
                1,
                608,
                220,
                1,
                518,
                338.5,
                1,
                646,
                247.5,
                1,
                576,
                395.5,
                1,
                431,
                211,
                1,
                414,
                251,
                1,
                304,
                220.5,
                1,
                275,
                265,
                1,
                201,
                211.5,
                1,
                154,
                266,
                1
            ],
            "track_id": 1,
            "image_id": 10003420058,
            "bbox": [
                80.19999999999999,
                129.62000356500002,
                639.5999999999999,
                300.55999596999993
            ],
            "scores": [],
            "category_id": 1,
            "id": 1000342005801,
            "iscrowd": false,
            "num_keypoints": 15
        },
        ...
    ],
    "categories": [
        {
            "supercategory": "person",
            "id": 1,
            "name": "person",
            "keypoints": [
                "nose",
                "head_bottom",
                "head_top",
                "left_ear",
                "right_ear",
                "left_shoulder",
                "right_shoulder",
                "left_elbow",
                "right_elbow",
                "left_wrist",
                "right_wrist",
                "left_hip",
                "right_hip",
                "left_knee",
                "right_knee",
                "left_ankle",
                "right_ankle"
            ],
            "skeleton": [
                [
                    16,
                    14
                ],
                [
                    14,
                    12
                ],
                [
                    17,
                    15
                ],
                [
                    15,
                    13
                ],
                [
                    12,
                    13
                ],
                [
                    6,
                    12
                ],
                [
                    7,
                    13
                ],
                [
                    6,
                    7
                ],
                [
                    6,
                    8
                ],
                [
                    7,
                    9
                ],
                [
                    8,
                    10
                ],
                [
                    9,
                    11
                ],
                [
                    2,
                    3
                ],
                [
                    1,
                    2
                ],
                [
                    1,
                    3
                ],
                [
                    2,
                    4
                ],
                [
                    3,
                    5
                ],
                [
                    4,
                    6
                ],
                [
                    5,
                    7
                ]
            ]
        }
    ]
}
```
