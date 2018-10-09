import xml.etree.ElementTree as ET
import cv2
import os


TRAIN_XML = "train.xml"
TEST_XML = "test.xml"
TRAIN_VIS_DIR = "train_vis"
TEST_VIS_DIR = "test_vis"


def draw_rectangle(image, x, y, w, h, tag):
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 1)
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.putText(image, tag, (x+2, y+h-2), font, 1, (0, 0, 255), 1)
    return image



def visualize(xml_file, vis_save_dir):
    if not os.path.exists(vis_save_dir):
        os.makedirs(vis_save_dir)
    count = 0
    root = ET.parse(xml_file).getroot()

    for image_node in root.findall("image"):
        image_path = image_node.find("imageName").text
        image = cv2.imread(image_path)
        
        for taggedRectangle_node in image_node.find("taggedRectangles").findall("taggedRectangle"):
            height = int(taggedRectangle_node.attrib["height"])
            width = int(taggedRectangle_node.attrib["width"])
            x = int(taggedRectangle_node.attrib["x"])
            y = int(taggedRectangle_node.attrib["y"])
            tag = taggedRectangle_node.find("tag").text
            count += 1
            draw_rectangle(image, x, y, width, height, tag)
        
        save_path = os.path.join(vis_save_dir, image_path.split("/")[-1])
        cv2.imwrite(save_path, image)


visualize(TRAIN_XML, TRAIN_VIS_DIR)
# visualize(TEST_XML, TEST_VIS_DIR)

