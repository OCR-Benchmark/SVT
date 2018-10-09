import xml.etree.ElementTree as ET
import cv2
import os


TRAIN_XML = "train.xml"
TEST_XML = "test.xml"
TRAIN_TAGS = "train.tags"
TEST_TAGS = "test.tags"
TRAIN_CROP_DIR = "train_crop"
TEST_CROP_DIR = "test_crop"
MARGIN_RATIO = 0


def crop_rectangle(image, x, y, w, h, margin_ratio=None):
    if margin_ratio is not None:
        img_h, img_w = image.shape[:2]
        plus_h = h * margin_ratio
        plus_w = w * margin_ratio
        x = max(x - int(plus_w / 2), 0)
        y = max(y - int(plus_h / 2), 0)
        w = int(w + plus_w)
        h = int(h + plus_h)
    return image[y:y+h, x:x+w]


def visualize(xml_file, crop_save_dir, tags_file):
    if not os.path.exists(crop_save_dir):
        os.makedirs(crop_save_dir)
    tags_fo = open(tags_file, "w")
    count = 0
    root = ET.parse(xml_file).getroot()

    for image_node in root.findall("image"):
        image_path = image_node.find("imageName").text
        image = cv2.imread(image_path)
        
        for i, taggedRectangle_node in enumerate(image_node.find("taggedRectangles").findall("taggedRectangle")):
            height = int(taggedRectangle_node.attrib["height"])
            width = int(taggedRectangle_node.attrib["width"])
            x = int(taggedRectangle_node.attrib["x"])
            y = int(taggedRectangle_node.attrib["y"])
            tag = taggedRectangle_node.find("tag").text.lower()
            count += 1
            image = crop_rectangle(image, x, y, width, height, margin_ratio=MARGIN_RATIO)
            save_path = os.path.join(crop_save_dir, image_path.split("/")[-1].replace(".jpg", "_{}.jpg".format(i)))
            cv2.imwrite(save_path, image)
            tags_fo.write("{} {}\n".format(os.path.abspath(save_path), tag))

    tags_fo.close()
    print(count)


# visualize(TRAIN_XML, TRAIN_CROP_DIR, TRAIN_TAGS)
visualize(TEST_XML, TEST_CROP_DIR, TEST_TAGS)

